./autogen.sh
# TODO --disable-wallet ?
./configure --without-gui --with-incompatible-bdb
make -j56
