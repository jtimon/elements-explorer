#! /usr/bin/env bash

# Causes the shell to exit if any subcommand or pipeline returns a non-zero status
set -e

REPO_HOST=${1}
REPO_NAME=${2}
BRANCH_DIR=$REPO_NAME-$BRANCH_COMMIT
BRANCH_URL=$REPO_HOST/$REPO_NAME/archive/$BRANCH_COMMIT.tar.gz
NUM_JOBS=4
if [ -f /proc/cpuinfo ]; then
    NUM_JOBS=$(cat /proc/cpuinfo | grep ^processor | wc -l)
fi

curl -L $BRANCH_URL | tar xz
cd $BRANCH_DIR
./autogen.sh
./configure --disable-wallet --without-gui --with-incompatible-bdb
make "src/"$REPO_NAME"d" -j$NUM_JOBS
