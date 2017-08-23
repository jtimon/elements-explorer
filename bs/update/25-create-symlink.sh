#!/bin/bash

# BSD="${BASEDIR}/${MODULE}"

[ ! -L $BSD ] && echo "BSD dir (${BSD}) doesn't exist" >&2 && exit 1;
[ ! -d ${DATDIR} ] && echo "DATDIR dir (${DATDIR}) doesn't exist" >&2 && exit 1;

DATDIR="/extra/explorer-data"
DATLINK=${BSD}/.explorer-data

rm -rf ${DATLINK}
[ -L ${DATLINK} ] && echo "Could not remove ${DATLINK}" >&2 && exit 1
mkdir ${DATLINK}

ln -s ${DATDIR}/bitcoin ${DATLINK}/bitcoin
ln -s ${DATDIR}/testnet3 ${DATLINK}/testnet3
ln -s ${DATDIR}/elementsregtest ${DATLINK}/elementsregtest
