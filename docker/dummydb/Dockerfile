FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python-pip

WORKDIR /build_docker

ADD docker/dummydb/requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt --require-hashes

ADD setup.py /build_docker/setup.py
ADD lib /build_docker/lib
RUN python /build_docker/setup.py develop
ADD py /build_docker/py

ADD docker/dummydb/Procfile /build_docker/docker/dummydb/Procfile
ADD docker/dummydb/.env /build_docker/docker/dummydb/.env
CMD honcho start -e docker/dummydb/.env -f docker/dummydb/Procfile
