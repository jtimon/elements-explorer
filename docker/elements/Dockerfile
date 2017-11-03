FROM ubuntu:16.04

WORKDIR /build_docker

ADD docker/daemon/deps.sh /build_docker/docker/daemon/deps.sh
RUN sh docker/daemon/deps.sh

RUN apt-get update && apt-get install -y python-pip
ADD docker/daemon/requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt --require-hashes

# Install elementsd with getperblockstats
ENV BRANCH_COMMIT=17613070a059aa6b9001af518f4de64ff6edcc2d
ENV REPO_HOST=https://github.com/jtimon
ENV DAEMON_NAME=elements
ENV MAKE_TARGET=src/elementsd

ADD docker/daemon/build.sh /build_docker/docker/daemon/build.sh
RUN sh /build_docker/docker/daemon/build.sh $REPO_HOST $DAEMON_NAME $BRANCH_COMMIT $MAKE_TARGET

ADD docker/$DAEMON_NAME/.env /build_docker/docker/$DAEMON_NAME/.env
ADD docker/$DAEMON_NAME/Procfile /build_docker/docker/$DAEMON_NAME/Procfile
CMD honcho start -e docker/$DAEMON_NAME/.env -f docker/$DAEMON_NAME/Procfile
