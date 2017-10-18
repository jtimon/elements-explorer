FROM ubuntu:16.04

WORKDIR /build_docker

RUN apt-get update && apt-get install -y python-pip
RUN pip install honcho

ADD docker/daemon-deps.sh /build_docker/docker/daemon-deps.sh
RUN sh docker/daemon-deps.sh

ADD docker/build-daemon.sh /build_docker/docker/build-daemon.sh
# Install elementsd with getperblockstats
RUN curl -L https://github.com/jtimon/elements/archive/e14-rpc-plotter.tar.gz | tar xz
RUN cd elements-e14-rpc-plotter && sh ./../docker/build-daemon.sh src/elementsd

EXPOSE 7041

ADD docker/elements/.env /build_docker/docker/elements/.env
ADD docker/elements/Procfile /build_docker/docker/elements/Procfile
CMD honcho start -e docker/elements/.env -f docker/elements/Procfile
