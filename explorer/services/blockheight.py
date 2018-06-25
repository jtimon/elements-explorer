
from mintools import minql

from explorer.models.block import Block

def GetBlockByHeight(rpccaller, height):
    try:
        block_by_height = Block.search({'height': height})
    except minql.NotFoundError:
        block_by_height = []
    except Exception as e:
        print("Error in GetBlockByHeight:", type(e), e)
        return {'error': {'message': 'Error getting block from db by height %s' % height}}
    if len(block_by_height) > 1:
        return {'error': {'message': 'More than one block cached for height %s' % height}}
    if len(block_by_height) == 1:
        return block_by_height[0]

    blockhash = rpccaller.RpcCall('getblockhash', {'height': height})
    if 'error' in blockhash:
        return blockhash
    block = Block.get(blockhash)
    if isinstance(block, dict) and 'error' in block:
        return block
    elif not isinstance(block, Block):
        print('Error in GetBlockByHeight: wrong type for block', blockhash, block)
        return {'error': {'message': 'Error getting block %s (by height %s)' % (blockhash, height)}}
    return block
