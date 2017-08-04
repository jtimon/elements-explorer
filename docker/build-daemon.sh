#! /usr/bin/env bash

# Causes the shell to exit if any subcommand or pipeline returns a non-zero status
set -e

DAEMON_TARGET=${1:-src/elementsd}
NUM_JOBS=4
if [ -f /proc/cpuinfo ]; then
    NUM_JOBS=$(cat /proc/cpuinfo | grep ^processor | wc -l)
fi

./autogen.sh
./configure --disable-wallet --without-gui --with-incompatible-bdb
make $DAEMON_TARGET -j$NUM_JOBS
