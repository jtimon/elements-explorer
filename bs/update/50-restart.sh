#!/bin/bash

cd /bs/rpc-explorer
make docker-down

# clean out old images
docker rmi $(sudo docker images -q)

make docker-build
