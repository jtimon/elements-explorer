#!/bin/sh

BRANCH_DIR=bitcoin-b15-rpc-explorer
DATADIR_MAIN=/root/.bitcoin/
PORT_MAIN=8532
DATADIR_TESTNET3=/root/.testnet3/
PORT_TESTNET3=18532

# TODO Use Honcho or supervisord instead of -daemon & (the logs for testnet3 get more hidden)
./$BRANCH_DIR/src/bitcoind -daemon -testnet -datadir=$DATADIR_TESTNET3 -printtoconsole -debug -logips -logtimestamps -server -txindex -rpcuser=user1 -rpcpassword=password1 -rpcallowip=10.5.0.5 -rpcbind=0.0.0.0:$PORT_TESTNET3 -listen -discover -persistmempool & \
./$BRANCH_DIR/src/bitcoind -datadir=$DATADIR_MAIN -rpcbind=0.0.0.0:$PORT_MAIN -printtoconsole -debug -logips -logtimestamps -server -txindex -rpcuser=user1 -rpcpassword=password1 -rpcallowip=10.5.0.5 -listen -discover -persistmempool
