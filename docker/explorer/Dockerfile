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

COPY docker/explorer/requirements.txt /build_docker/requirements.txt
RUN pip install -r requirements.txt --require-hashes

# upgrade node (need to downgrade npm first)
RUN npm install -g npm@4.6.1
RUN npm install -g n
RUN n 10.0.0
RUN npm install -g npm@6.0.0

COPY docker/explorer/package.json /build_docker/gui_alt/package.json
RUN cd gui_alt && npm i --production
COPY gui2/package.json /build_docker/gui2/package.json
RUN cd gui2 && npm i --production

COPY mintools /build_docker/mintools
COPY explorer /build_docker/explorer
COPY setup.py /build_docker/setup.py
RUN python /build_docker/setup.py develop

COPY webflask /build_docker/webflask
COPY gui_alt /build_docker/gui_alt
COPY gui2 /build_docker/gui2
RUN cd gui2 && npm run build

COPY docker/conf/explorer.proc /build_docker/docker/conf/explorer.proc
COPY docker/conf/explorer.env /build_docker/docker/conf/explorer.env
CMD honcho start -e docker/conf/explorer.env -f docker/conf/explorer.proc
