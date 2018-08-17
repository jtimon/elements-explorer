#! /usr/bin/env bash

# Causes the shell to exit if any subcommand or pipeline returns a non-zero status
set -e

# $1=BRANCH_COMMIT $2=REPO_NAME $3=REPO_HOST $4=DAEMON_NAME

if [ "$4" = "" -o "$4" = "disabled_daemon" ]; then
    exit 0
fi

BRANCH_DIR=$2-$1
BRANCH_URL=$3/$2/archive/$1.tar.gz
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
make "src/"$4"d" -j$NUM_JOBS
make "src/"$4"-cli" -j$NUM_JOBS
