#!/bin/sh

BRANCH_DIR=bitcoin-b15-rpc-explorer

# TODO Use Honcho or supervisord instead of -daemon & (the logs for testnet3 get more hidden)
# ./$BRANCH_DIR/src/bitcoind -daemon -testnet -datadir=/root/.testnet3/ -printtoconsole -debug -logips -logtimestamps -server -txindex -rpcuser=user1 -rpcpassword=password1 -rpcallowip=10.5.0.5 -rpcbind=0.0.0.0:18332 -listen -discover & \
./$BRANCH_DIR/src/bitcoind -datadir=/root/.bitcoin/ -printtoconsole -debug -logips -logtimestamps -server -txindex -rpcuser=user1 -rpcpassword=password1 -rpcallowip=10.5.0.5 -rpcbind=0.0.0.0:8332 -listen -discover
