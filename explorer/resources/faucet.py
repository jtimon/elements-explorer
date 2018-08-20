# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime

import mintools

from explorer.models.faucet import Faucetsent

from .chain import UnknownChainError, ChainResource

COIN = 100000000
MIN_KEEP = 0.5
MIN_SATOSHIS_SEND = 1000
MAX_SATOSHIS_SEND = COIN

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

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        request = req['json']
        if not 'address' in request:
            return {'error': {'message': 'No address specified to get %s in request %s' % ('freecoins', request)}}, 400

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

        hours_ago = 24
        seconds_ago = hours_ago * 60 * 60
        min_epoch = int((datetime.datetime.now() - datetime.timedelta(seconds=seconds_ago)).strftime('%s'))
        recent_sends = Faucetsent.search({'ip': req['ip'], 'time': {'ge': min_epoch}})
        if len(recent_sends) > 0:
            return {'error': {'message': "freecoins: Coins were given to ip %s in the last %s hours (chain %s)" % (
                req['ip'], hours_ago, self.chain)}}, 400
        
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
