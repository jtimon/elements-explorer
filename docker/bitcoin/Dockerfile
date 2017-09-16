FROM ubuntu:16.04

WORKDIR /build_docker

ADD docker/daemon-deps.sh /build_docker/docker/daemon-deps.sh
RUN sh docker/daemon-deps.sh

ADD docker/build-daemon.sh /build_docker/docker/build-daemon.sh
# Install bitcoind with getperblockstats
RUN curl -L https://github.com/jtimon/bitcoin/archive/b15-rpc-explorer.tar.gz | tar xz
RUN cd bitcoin-b15-rpc-explorer && sh ./../docker/build-daemon.sh src/bitcoind

EXPOSE 8532
EXPOSE 18532

ADD docker/bitcoin/start.sh /build_docker/docker/bitcoin/start.sh
CMD ["sh", "docker/bitcoin/start.sh"]
