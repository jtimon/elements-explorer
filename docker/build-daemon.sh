./autogen.sh
# TODO --disable-wallet ?
./configure --without-gui --with-incompatible-bdb

NUM_JOBS=4
if [ -f /proc/cpuinfo ]; then
    NUM_JOBS=$(cat /proc/cpuinfo | grep ^processor | wc -l)
fi
 
make -j$NUM_JOBS
