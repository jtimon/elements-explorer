FROM ubuntu:16.04

WORKDIR /build_docker

ADD docker/daemon/deps.sh /build_docker/docker/daemon/deps.sh
RUN sh docker/daemon/deps.sh

RUN apt-get update && apt-get install -y python-pip
ADD docker/daemon/requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt --require-hashes

# Install bitcoind with getperblockstats
ENV BRANCH_COMMIT=44dcea038b44890e5f49c71ff26cfcb4ecf0da15
ENV REPO_HOST=https://github.com/jtimon
ENV DAEMON_NAME=bitcoin
ENV MAKE_TARGET=src/bitcoind

ADD docker/daemon/build.sh /build_docker/docker/daemon/build.sh
RUN sh /build_docker/docker/daemon/build.sh $REPO_HOST $DAEMON_NAME

ADD docker/$DAEMON_NAME/.env /build_docker/docker/$DAEMON_NAME/.env
ADD docker/$DAEMON_NAME/Procfile /build_docker/docker/$DAEMON_NAME/Procfile
CMD honcho start -e docker/$DAEMON_NAME/.env -f docker/$DAEMON_NAME/Procfile
