# rpc-explorer

A simple block explorer based on deamon's rpc calls.

# Dependencies:

## Fundamental dependencies:

Dependent on the OS distribution:

```
make, python, pip, virtualenv
```

## Installation

To install the python server:

```
make
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
make run
```

Check the python server is properly running with:

```
curl  --data-binary '{"chain": "betaregtest", "jsonrpc": "1.0", "id":"curltest", "method": "getblockchaininfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:5000/rpcexplorerrest
```

Run `grunt` for building and `grunt serve` for preview.

Once the bower components have been installed (run grunt once), you can also test the web
without grunt just going to http://127.0.0.1:5000 (as noted by the python server).

## TODO Angular/Karma/Protractor/e2e Testing

Running `grunt test` will run the unit tests with karma.

## TODO

- [x] Whitelist rpc calls from python server (only the few needed ones)
- [x] Select chain
- [x] Hide non interesting things for coinbase inputs and their complement
- [x] Hide or show CT/non-CT values in a more beauty way
- [x] Hide non interesting things for betad chains (pow vs signblock, covered above besides the fields hidden in verbose)
- [ ] Move from bower to webpack
- [ ] Move from npm to webpack
- [ ] Fix Grunt
- [ ] Move from grunt to gulp
- [ ] Move from angular to React + redux
- [ ] Cleanup error display
- [ ] Show -signblockscript and block.scriptSig
- [ ] Show -fedpegscript
- [ ] Angular directive for both scriptSig and scriptPubKey
- [ ] Not hardcoded rpcuser/rpcpassword:
- [ ] Deploy in blockstream servers
- [ ] Hide non interesting things for bitcoind chains
- [ ] Adapt to elementsd chains (both show/hide)
- [ ] Make sure we're not missing data from differences in chains
- [ ] Make sure there's nothing to rescue from 'verbose' even after supporting some other elements chain

# License

MIT, see COPYRIGHT.md
