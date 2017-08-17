#!/bin/bash

MODULE="rpc-explorer"
BRANCH="staging"

cat <<EOF > /root/.ssh/config
host gl
 HostName gl.blockstream.io
 IdentityFile ~/.ssh/deploy_key
 User git
EOF

mkdir -p /bs/.scaffold/config/releases
cd /bs/.scaffold/config/
git clone --branch ${BRANCH} git@gl:liquid/${MODULE} MASTER

DS=$(date +%Y%m%y%H%M%S)

git clone MASTER releases/${MODULE}-${DS}
ln -s /bs/.scaffold/config/releases/${MODULE}-${DS} /bs/${MODULE}

exit 0
