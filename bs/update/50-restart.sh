#!/bin/bash

cd /bs/elemenets-explorer

# clean out old images
docker rmi $(sudo docker images -q)

make staging
