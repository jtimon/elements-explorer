#!/bin/bash

# BSD="${BASEDIR}/${MODULE}"

[ ! -L $BSD ] && echo "BSD dir (${BSD}) doesn't exist" >&2 && exit 1;
[ ! -d ${DATDIR} ] && echo "DATDIR dir (${DATDIR}) doesn't exist" >&2 && exit 1;

DATDIR="/extra/explorer-data"
DATLINK=${BSD}/.explorer-dat

rm -f ${DATLINK}
[ -L ${DATLINK} ] && echo "Could not remove ${DATLINK}" >&2 && exit 1

ln -s ${DATDIR} ${DATLINK}
