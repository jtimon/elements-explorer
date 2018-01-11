#!/bin/bash

cd /bs/rpc-explorer

# clean out old images
docker rmi $(sudo docker images -q)

make staging
