#! /usr/bin/env bash

# Causes the shell to exit if any subcommand or pipeline returns a non-zero status
set -e

BRANCH_DIR=$REPO_NAME-$BRANCH_COMMIT
BRANCH_URL=$REPO_HOST/$REPO_NAME/archive/$BRANCH_COMMIT.tar.gz
NUM_JOBS=4
if [ -f /proc/cpuinfo ]; then
    NUM_JOBS=$(cat /proc/cpuinfo | grep ^processor | wc -l)
fi

apt-get update
apt-get install -yqq libdb-dev libdb++-dev

curl -L $BRANCH_URL | tar xz
cd $BRANCH_DIR
./autogen.sh
./configure --without-gui --with-incompatible-bdb
make "src/"$DAEMON_NAME"d" -j$NUM_JOBS
make "src/"$DAEMON_NAME"-cli" -j$NUM_JOBS
