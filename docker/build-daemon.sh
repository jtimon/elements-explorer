./autogen.sh
./configure --disable-wallet --without-gui --with-incompatible-bdb

DAEMON_TARGET=${1:-src/elementsd}
NUM_JOBS=4
if [ -f /proc/cpuinfo ]; then
    NUM_JOBS=$(cat /proc/cpuinfo | grep ^processor | wc -l)
fi

make $DAEMON_TARGET -j$NUM_JOBS
