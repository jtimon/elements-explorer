FROM ubuntu:16.04

EXPOSE 5000

RUN apt-get update
RUN apt-get install -y nodejs npm python-pip git

WORKDIR /build_docker

ADD app/package.json /build_docker/app/package.json
RUN cd app && npm i

ADD requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt

ADD py /build_docker/py
ADD app /build_docker/app
ADD docker/explorer/start.sh /build_docker/docker/explorer/start.sh
CMD ["sh", "docker/explorer/start.sh"]
