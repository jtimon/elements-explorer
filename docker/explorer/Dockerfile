FROM ubuntu:16.04

EXPOSE 5000

RUN apt-get update && apt-get install -y \
    git \
    nodejs \
    npm \
    python-pip \
    python-dev \
    libpq-dev \
    postgresql-server-dev-all

WORKDIR /build_docker

ADD docker/explorer/package.json /build_docker/gui/package.json
RUN cd gui && npm i

ADD docker/explorer/requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt --require-hashes

ADD setup.py /build_docker/setup.py
ADD lib /build_docker/lib
RUN python /build_docker/setup.py develop
ADD webflask /build_docker/webflask
ADD gui /build_docker/gui
ADD docker/explorer/Procfile /build_docker/docker/explorer/Procfile
ADD docker/explorer/.env /build_docker/docker/explorer/.env
CMD honcho start -e docker/explorer/.env -f docker/explorer/Procfile
