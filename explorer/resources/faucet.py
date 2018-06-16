
import datetime

from mintools import minql

from explorer import models

from .chain import UnknownChainError, ChainResource

COIN = 100000000
MIN_KEEP = 10

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
    return float(satoshis / COIN)
    

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

        print('Faucet: Sending %s to %s' % (amount, address))
        txid = self.rpccaller.RpcCall('sendtoaddress', {'address': address, 'amount': str(amount)})
        if 'error' in txid:
            return {'error': txid['error']}, 400

        return {
            'address': address,
            'amount': amount,
            'time': datetime.datetime.now(),
            'txid': txid,
        }, 200
