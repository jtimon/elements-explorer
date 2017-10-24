FROM ubuntu:16.04

WORKDIR /build_docker

ADD docker/daemon-deps.sh /build_docker/docker/daemon-deps.sh
RUN sh docker/daemon-deps.sh

ADD docker/build-daemon.sh /build_docker/docker/build-daemon.sh
# Install elementsd with getperblockstats
RUN curl -L https://github.com/jtimon/elements/archive/17613070a059aa6b9001af518f4de64ff6edcc2d.tar.gz | tar xz
RUN cd elements-17613070a059aa6b9001af518f4de64ff6edcc2d && sh ./../docker/build-daemon.sh src/elementsd

RUN apt-get update && apt-get install -y python-pip

ADD docker/daemon-requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt --require-hashes

ADD docker/elements/.env /build_docker/docker/elements/.env
ADD docker/elements/Procfile /build_docker/docker/elements/Procfile
CMD honcho start -e docker/elements/.env -f docker/elements/Procfile
