FROM ubuntu:16.04

WORKDIR /build_docker

ADD docker/daemon-deps.sh /build_docker/docker/daemon-deps.sh
RUN sh docker/daemon-deps.sh

RUN apt-get update && apt-get install -y python-pip
ADD docker/daemon-requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt --require-hashes

# Install elementsd with getperblockstats
ENV BRANCH_COMMIT=17613070a059aa6b9001af518f4de64ff6edcc2d
ENV DAEMON_NAME=elements
ENV DAEMON_D=src/elementsd
ENV BRANCH_URL=https://github.com/jtimon/$DAEMON_NAME/archive/$BRANCH_COMMIT.tar.gz
ENV BRANCH_DIR=$DAEMON_NAME-$BRANCH_COMMIT

ADD docker/build-daemon.sh /build_docker/docker/build-daemon.sh
RUN curl -L $BRANCH_URL | tar xz
RUN cd $BRANCH_DIR && sh ./../docker/build-daemon.sh $DAEMON_D

ADD docker/$DAEMON_NAME/.env /build_docker/docker/$DAEMON_NAME/.env
ADD docker/$DAEMON_NAME/Procfile /build_docker/docker/$DAEMON_NAME/Procfile
CMD honcho start -e docker/$DAEMON_NAME/.env -f docker/$DAEMON_NAME/Procfile
