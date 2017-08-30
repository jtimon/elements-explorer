#!/bin/sh

BRANCH_DIR=elements-e14-rpc-plotter
DATADIR=/root/.elements/
PORT=7041

# TODO Use Honcho or supervisord
./$BRANCH_DIR/src/elementsd -regtest -datadir=$DATADIR -rpcbind=0.0.0.0:$PORT -printtoconsole -debug -logips -logtimestamps -server -txindex -rpcuser=user1 -rpcpassword=password1 -rpcallowip=10.5.0.5 -listen -discover -validatepegin=0
