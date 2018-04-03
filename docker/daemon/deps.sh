#! /usr/bin/env bash

# Causes the shell to exit if any subcommand or pipeline returns a non-zero status
set -e

# sed -i 's/deb.debian.org/httpredir.debian.org/g' /etc/apt/sources.list
apt-get update
apt-get install -yqq curl
apt-get install -yqq make build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev libminiupnpc-dev libzmq3-dev
# apt-get install -yqq python curl build-essential libtool autotools-dev automake pkg-config bsdmainutils
# rm -rf /var/lib/apt/lists/* /var/cache/* /tmp/* /usr/share/locale/* /usr/man /usr/share/doc /lib/xtables/libip6*
