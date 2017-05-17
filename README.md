# rpc-explorer

A simple block explorer based on deamon's rpc calls.

## Installation

To install the python server:

```
pip install -r requirements.txt
```

To install the javascript requirements:

```
npm install
```

## Build & development

This needs a Bitcoin, Elements or compatible deamon running alongside
it in the same machine with at least the following in its
configuration file:

```
server=1
txindex=1
rpcuser=user1
rpcpassword=password1
```

Run the daemon, examples:
```
./betad -daemon -regtest -conf=betaregtest.conf
./betad -daemon -testnet -conf=betatestnet3.conf
./betad -daemon -conf=liquid.conf
./bitcoind -daemon -testnet -conf=testnet3.conf
./bitcoind -daemon -conf=explorer.conf -datadir=$BTCTXINDEX_DATADIR
```

Run the http server:

```
python ./py/__init__.py
```

Check the python server is properly running with:

```
curl  --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:5000/bitcoind
```

Run `grunt` for building and `grunt serve` for preview.

## Testing

Running `grunt test` will run the unit tests with karma.

## TODO

- [x] Whitelist rpc calls from python server (only the few needed ones)
- [x] Select chain
- [x] Hide non interesting things for coinbase inputs and their complement
- [ ] Cleanup error display
- [ ] Hide non interesting things for betad chains
- [ ] Hide or show CT/non-CT values in a more beauty way
- [ ] Show -signblockscript and block.scriptSig
- [ ] Show -fedpegscript
- [ ] Angular directive for both scriptSig and scriptPubKey
- [ ] Not hardcoded rpcuser/rpcpassword:
- [ ] Deploy in blockstream servers
- [ ] Hide non interesting things for bitcoind chains
- [ ] Adapt to elementsd chains (both show/hide)
- [ ] Make sure we're not missing data from differences in chains
