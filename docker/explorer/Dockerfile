FROM ubuntu:16.04

EXPOSE 5000

RUN apt-get update && apt-get install -y \
    curl \
    git \
    nodejs \
    npm \
    python-pip \
    python-dev \
    libpq-dev \
    postgresql-server-dev-all

WORKDIR /build_docker

# Or install nodejs-legacy to avoid the symlink
RUN ln -s /usr/bin/nodejs /usr/bin/node

# upgrade node (need to downgrade npm first)
RUN npm install -g npm@4.6.1
RUN npm install -g n
RUN n stable
RUN npm install -g npm

ADD docker/explorer/package.json /build_docker/gui/package.json
RUN cd gui && npm i --production
ADD gui2/package.json /build_docker/gui2/package.json
RUN cd gui2 && npm i --production

ADD docker/explorer/requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt --require-hashes

ADD mintools /build_docker/mintools
ADD explorer /build_docker/explorer
ADD setup.py /build_docker/setup.py
RUN python /build_docker/setup.py develop
ADD webflask /build_docker/webflask
ADD gui /build_docker/gui
ADD gui2 /build_docker/gui2
RUN cd gui2 && npm run build

ADD docker/conf/explorer.proc /build_docker/docker/conf/explorer.proc
ADD docker/conf/explorer.env /build_docker/docker/conf/explorer.env
CMD honcho start -e docker/conf/explorer.env -f docker/conf/explorer.proc
