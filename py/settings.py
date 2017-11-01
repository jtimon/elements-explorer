
import os

CLIENT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'app')

WEB_ALLOWED_CALLS = [
    'block', # cached in server and gui
    'tx', # cached in server and gui
    'blockstats', # cached in server and gui
    "getblockchaininfo", # cached in gui (TODO subscribe from gui)
    "getblockhash", # never cached, always hits the node
    "getmempoolinfo", # never cached, always hits the node
    "getrawmempool", # never cached, always hits the node
    "getmempoolentry", # never cached, always hits the node
]
