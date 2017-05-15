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
./bitcoind -daemon
./elementsd -daemon -server=1 -txindex=1 -rpcuser=user1 -rpcpassword=password1 validatepegout=0
./betad -daemon -chain=betaregtest -conf=beta.conf
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

- [ ] Select chain
- [ ] Whitelist rpc calls from python server (only the few needed ones)
- [ ] Not hardcoded rpcuser/rpcpassword:
