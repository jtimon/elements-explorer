FROM ubuntu:18.04

WORKDIR /build_docker

COPY docker/daemon/deps.sh /build_docker/docker/daemon/deps.sh
RUN sh docker/daemon/deps.sh

RUN apt-get update && apt-get install -qfy python-pip
COPY docker/daemon/requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt --require-hashes

COPY docker/daemon/build-with-wallet.sh /build_docker/docker/daemon/build-with-wallet.sh

# Install bitcoind from ElementsProject/pre-elements-0.16
ARG CORE_DAEMON_NAME
ENV CORE_BRANCH_COMMIT=8b0085f82ade76cea322a1c3ff2486f4333de252
ENV CORE_REPO_HOST=https://github.com/ElementsProject
ENV CORE_REPO_NAME=elements
RUN sh /build_docker/docker/daemon/build-with-wallet.sh $CORE_BRANCH_COMMIT $CORE_REPO_NAME $CORE_REPO_HOST $CORE_DAEMON_NAME

# Install elementsd
ARG ELEMENTS_DAEMON_NAME
ENV ELEMENTS_BRANCH_COMMIT=58dee91e37454282c3fcf1b20ed526c594e1ebd2
ENV ELEMENTS_REPO_HOST=https://github.com/jtimon
ENV ELEMENTS_REPO_NAME=elements
RUN sh /build_docker/docker/daemon/build-with-wallet.sh $ELEMENTS_BRANCH_COMMIT $ELEMENTS_REPO_NAME $ELEMENTS_REPO_HOST $ELEMENTS_DAEMON_NAME

# Install bitcoind from ElementsProject/signet
# TODO maintain only one branch directly on top of bitcoin core's master
ENV SIGNET_BRANCH_COMMIT=1530cf40d60da34b6b46ea2bbe1e93bbb45615dc
RUN sh /build_docker/docker/daemon/build-with-wallet.sh $SIGNET_BRANCH_COMMIT $CORE_REPO_NAME $CORE_REPO_HOST $CORE_DAEMON_NAME

ARG ENV_NAME
COPY docker/$ENV_NAME/conf/torrc /etc/torrc
COPY docker/$ENV_NAME/conf/daemons.env /build_docker/docker/conf/daemons.env
COPY docker/$ENV_NAME/conf/daemons.proc /build_docker/docker/conf/daemons.proc
CMD honcho start -e docker/conf/daemons.env -f docker/conf/daemons.proc
