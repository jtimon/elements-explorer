FROM ubuntu:16.04

WORKDIR /build_docker

RUN apt-get update && apt-get install -y python-pip
RUN pip install honcho

ADD docker/daemon-deps.sh /build_docker/docker/daemon-deps.sh
RUN sh docker/daemon-deps.sh

ADD docker/build-daemon.sh /build_docker/docker/build-daemon.sh
# Install bitcoind with getperblockstats
RUN curl -L https://github.com/jtimon/bitcoin/archive/caeaf86de426f9b71c0828be23253827dd0149fb.tar.gz | tar xz
RUN cd bitcoin-caeaf86de426f9b71c0828be23253827dd0149fb && sh ./../docker/build-daemon.sh src/bitcoind

EXPOSE 8532
EXPOSE 18532

ADD docker/bitcoin/.env /build_docker/docker/bitcoin/.env
ADD docker/bitcoin/Procfile /build_docker/docker/bitcoin/Procfile
CMD honcho start -e docker/bitcoin/.env -f docker/bitcoin/Procfile
