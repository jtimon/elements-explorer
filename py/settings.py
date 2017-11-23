
import os

CLIENT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'app')

WEB_ALLOWED_CALLS = [
    'block', # cached in server and gui
    'tx', # cached in server and gui
    'blockstats', # cached in server and gui
    # cached in gui (TODO handle reorgs from gui)
    'chaininfo', # cached in server, reorgs handled with zmq subscription to node
    "blockhash", # cached in server, reorgs handled with zmq subscription to node
    'mempoolstats', # Data from db, independent from reorgs
    "getmempoolinfo", # never cached, always hits the node
    "getrawmempool", # never cached, always hits the node
    "getmempoolentry", # never cached, always hits the node
]
