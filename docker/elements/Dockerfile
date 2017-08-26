FROM ubuntu:16.04

# Set the working directory to /build_docker
WORKDIR /build_docker
# Copy the current directory contents into the container at /build_docker
ADD . /build_docker

RUN sh docker/daemon-deps.sh

# Install elementsd with getperblockstats
RUN curl -L https://github.com/jtimon/elements/archive/e14-rpc-plotter.tar.gz | tar xz
RUN cd elements-e14-rpc-plotter && sh ./../docker/build-daemon.sh src/elementsd

EXPOSE 7041

CMD ["sh", "docker/elements/start.sh"]
