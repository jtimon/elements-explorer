# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import json
import requests

import mintools

from explorer.models.faucet import Faucetsent
from explorer.env_config import FAUCET_SECONDS_AGO

from .chain import UnknownChainError, ChainResource

COIN = 100000000
MIN_KEEP = 0.5
MIN_SATOSHIS_SEND = 1000
MAX_SATOSHIS_SEND = COIN

# Load RECAPTCHA_SECRET or use not working default
try:
    with open('/build_docker/keys/RECAPTCHA_SECRET.txt', 'r') as f:
        recaptcha_list = f.read().splitlines()
        assert len(recaptcha_list) == 1
        RECAPTCHA_SECRET = recaptcha_list[0]
        print('BlockGenerator.import_keys_if_any: Rpc importprivkey result', result)
except IOError:
    print('ERROR: File /build_docker/keys/RECAPTCHA_SECRET.txt not found. Using public default...')
    RECAPTCHA_SECRET = 'no_recaptcha'

def get_balance(rpccaller, chain):
    balance_dict = rpccaller.RpcCall('getbalance', {})
    print('Faucet balance for chain %s:' % chain, balance_dict)
    if isinstance(balance_dict, float):
        return balance_dict
    elif isinstance(balance_dict, basestring):
        return float(balance_dict)
    elif isinstance(balance_dict, dict) and  'bitcoin' in balance_dict:
        return float(balance_dict['bitcoin'])
    return 0

def get_amount(balance):
    if balance <= MIN_KEEP:
        return 0
    satoshis = int((balance / 10000) * COIN)
    if satoshis < MIN_SATOSHIS_SEND:
        return 0
    elif satoshis > MAX_SATOSHIS_SEND:
        satoshis = MAX_SATOSHIS_SEND
    return satoshis / float(COIN)


class FaucetInfoResource(ChainResource):

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        balance = get_balance(self.rpccaller, self.chain)
        amount = get_amount(balance)

        newaddress = self.rpccaller.RpcCall('getnewaddress', {})
        if 'error' in newaddress:
            return {'error': newaddress['error']}, 400

        return {
            'amount': amount,
            'balance': balance,
            'donation_address': newaddress,
            'time': datetime.datetime.now(),
        }, 200

class FreeCoinsResource(ChainResource):

    def check_recaptcha_response():
        if not 'g-recaptcha-response' in request:
            return {'error': {'message': 'No g-recaptcha-response specified to get %s in request %s' % ('freecoins', request)}}, 400

        r = requests.post("https://www.google.com/recaptcha/api/siteverify",
                          data={'secret': RECAPTCHA_SECRET,
                                'response': request['g-recaptcha-response'],
                                'remoteip': req['ip']
                          })
        print(r.status_code, r.reason)
        if r.status_code != 200:
            return {'error': {'message': '%s: Recaptcha failed %s' % ('freecoins', r.reason)}}, 400

        print(r.text)
        try:
            recaptcha_response = json.loads(r.text)
        except Exception as e:
            print("Error in FreeCoinsResource:", type(e), e)
            return {'error': {'message': '%s: Recaptcha failed %s' % ('freecoins', r.text)}}, 400

        if not 'success' in recaptcha_response or not recaptcha_response['success']:
            return {'error': {'message': '%s: Recaptcha failed %s' % ('freecoins', r.text)}}, 400
        return {}

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        if not 'ip' in req:
            return {'error': {'message': 'No ip specified to get %s in request %s' % ('freecoins', req)}}, 400

        request = req['json']
        if not 'address' in request:
            return {'error': {'message': 'No address specified to get %s in request %s' % ('freecoins', request)}}, 400

        if RECAPTCHA_SECRET != 'no_recaptcha':
            response = self.check_recaptcha_response()
            if 'error' in response:
                return {'error': {'message': '%s: Recaptcha failed: %s' % ('freecoins', response['error'])}}, 400

        address = request['address']
        balance = get_balance(self.rpccaller, self.chain)
        amount = get_amount(balance)

        if amount <= 0:
            return {'error': {'message': '%s: Not enough funds for chain %s' % ('freecoins', self.chain)}}, 400

        try:
            Faucetsent.get(address)
            return {'error': {'message': "%s: Don't reuse address %s (chain %s)" % ('freecoins', address, self.chain)}}, 400
        except mintools.minql.NotFoundError:
            pass

        min_epoch = int((datetime.datetime.now() - datetime.timedelta(seconds=FAUCET_SECONDS_AGO)).strftime('%s'))
        recent_sends = Faucetsent.search({'ip': req['ip'], 'time': {'ge': min_epoch}})
        if len(recent_sends) > 0:
            return {'error': {'message': "freecoins: Coins were given to ip %s in the last %s seconds (chain %s)" % (
                req['ip'], FAUCET_SECONDS_AGO, self.chain)}}, 400

        print('Faucet: Sending %s to %s' % (amount, address))
        txid = self.rpccaller.RpcCall('sendtoaddress', {'address': address, 'amount': str(amount)})
        if 'error' in txid:
            return {'error': txid['error']}, 400

        faucetsent = Faucetsent(json_dict={
            'address': address,
            'amount': amount,
            'ip': req['ip'],
            'time': int(datetime.datetime.now().strftime('%s')),
            'txid': txid,
        })
        faucetsent.save()
        return faucetsent.json(), 200
