FROM ubuntu:16.04

WORKDIR /build_docker

ADD docker/daemon-deps.sh /build_docker/docker/daemon-deps.sh
RUN sh docker/daemon-deps.sh

ADD docker/build-daemon.sh /build_docker/docker/build-daemon.sh
# Install elementsd with getperblockstats
RUN curl -L https://github.com/jtimon/elements/archive/e14-rpc-plotter.tar.gz | tar xz
RUN cd elements-e14-rpc-plotter && sh ./../docker/build-daemon.sh src/elementsd

EXPOSE 7041

ADD docker/bitcoin/start.sh /build_docker/docker/bitcoin/start.sh
CMD ["sh", "docker/elements/start.sh"]
