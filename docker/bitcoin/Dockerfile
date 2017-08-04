FROM ubuntu:16.04

# Set the working directory to /build_docker
WORKDIR /build_docker
# Copy the current directory contents into the container at /build_docker
ADD . /build_docker

RUN sh docker/daemon-deps.sh

# Install bitcoind with getperblockstats
RUN git clone https://github.com/jtimon/bitcoin.git --single-branch --branch b15-rpc-explorer
ADD . /build_docker

RUN cd bitcoin && sh ./../docker/build-daemon.sh src/bitcoind
ADD . /build_docker

EXPOSE 8332
EXPOSE 18332

CMD ["sh", "docker/bitcoin/start.sh"]
