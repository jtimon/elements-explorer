FROM ubuntu:16.04

WORKDIR /build_docker

ADD docker/daemon-deps.sh /build_docker/docker/daemon-deps.sh
RUN sh docker/daemon-deps.sh

RUN apt-get update && apt-get install -y python-pip
ADD docker/daemon-requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt --require-hashes

# Install bitcoind with getperblockstats
ENV BRANCH_COMMIT=624dfc78b18ea9089ba198c016fe36310a6a10a4
ENV DAEMON_NAME=bitcoin
ENV DAEMON_D=src/bitcoind
ENV BRANCH_URL=https://github.com/jtimon/$DAEMON_NAME/archive/$BRANCH_COMMIT.tar.gz
ENV BRANCH_DIR=$DAEMON_NAME-$BRANCH_COMMIT

ADD docker/build-daemon.sh /build_docker/docker/build-daemon.sh
RUN curl -L $BRANCH_URL | tar xz
RUN cd $BRANCH_DIR && sh ./../docker/build-daemon.sh $DAEMON_D

ADD docker/$DAEMON_NAME/.env /build_docker/docker/$DAEMON_NAME/.env
ADD docker/$DAEMON_NAME/Procfile /build_docker/docker/$DAEMON_NAME/Procfile
CMD honcho start -e docker/$DAEMON_NAME/.env -f docker/$DAEMON_NAME/Procfile
