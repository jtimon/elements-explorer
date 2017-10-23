FROM ubuntu:16.04

EXPOSE 5000

RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    python-pip \
    git

WORKDIR /build_docker

ADD docker/explorer/package.json /build_docker/app/package.json
RUN cd app && npm i

ADD requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt --require-hashes

ADD setup.py /build_docker/setup.py
ADD lib /build_docker/lib
RUN python /build_docker/setup.py develop
ADD py /build_docker/py
ADD app /build_docker/app
ADD docker/explorer/Procfile /build_docker/docker/explorer/Procfile
ADD docker/explorer/.env /build_docker/docker/explorer/.env
CMD honcho start -e docker/explorer/.env -f docker/explorer/Procfile
