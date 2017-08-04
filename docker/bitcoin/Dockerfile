FROM ubuntu:16.04

# Set the working directory to /build_docker
WORKDIR /build_docker
# Copy the current directory contents into the container at /build_docker
ADD . /build_docker

RUN sh docker/daemon-deps.sh

# Install bitcoind with getperblockstats
RUN curl -L https://github.com/jtimon/bitcoin/archive/b15-rpc-explorer.tar.gz | tar xz
ADD . /build_docker

RUN cd bitcoin-b15-rpc-explorer && sh ./../docker/build-daemon.sh src/bitcoind
ADD . /build_docker

EXPOSE 8332
EXPOSE 18332

CMD ["sh", "docker/bitcoin/start.sh"]
