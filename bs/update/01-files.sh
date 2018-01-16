#!/bin/bash

echo "rsync'ing files in from the got repo..."

BASEDIR="/bs/elements-explorer/bs"

if [ -d $BASEDIR/files ]; then
	cd /
	rsync -av $BASEDIR/files/ .
fi
