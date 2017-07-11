FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y git

RUN apt-get update
RUN apt-get install -y software-properties-common

RUN add-apt-repository -y ppa:bitcoin/bitcoin
RUN apt-get update
RUN apt-get install -y make build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev libminiupnpc-dev libzmq3-dev
RUN apt-get install -y libdb4.8-dev libdb4.8++-dev

# Set the working directory to /build_docker
WORKDIR /build_docker

# Copy the current directory contents into the container at /build_docker
ADD . /build_docker

# Install elementsd with getperblockstats
RUN git clone https://github.com/jtimon/elements.git --single-branch --branch e14-rpc-plotter
ADD . /build_docker

# TODO --disable-wallet ?
RUN cd elements && ./autogen.sh ;
RUN cd elements && ./configure --without-gui --with-incompatible-bdb ;
# TODO --disable-wallet ?
ADD . /build_docker

RUN cd elements && make -j56 ;
ADD . /build_docker

EXPOSE 7041

CMD ["./elements/src/elementsd", "-regtest", "-printtoconsole", "-debug", "-logips", "-logtimestamps", "-server", "-txindex", "-rpcuser=user1", "-rpcpassword=password1", "-rpcallowip=10.5.0.5", "-rpcbind=0.0.0.0:7041", "-listen", "-discover"]
