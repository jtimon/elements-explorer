# rpc-explorer

A simple block explorer based on deamon's rpc calls.

# Dependencies: #

Dependent on the OS distribution:

```
make python docker-ce docker-compose
```

Docker-compose should be installed with pip: 

```
sudo pip uninstall docker-compose
sudo pip install -U docker-compose
```

Add your user to the docker group:

```
sudo usermod -a -G docker $USER
```

Restart the system for the last command to take effect.

Test docker installation:

```
docker run hello-world
```

# Build & development #

To build and run:

```
cd docker
docker-compose up --build
```

Visit the local web going to http://127.0.0.1:5000

If you prefer it to be run as a daemon use:

```
docker-compose up --build -d
```

## TODO Closing ##

Before closing down the whole docker project, close the bitcoin daemon manually:

```
docker ps -a
docker attach rpcexplorer_bitcoin_1
Ctrl-c, Ctrl-c
```
Or just mind .bitcoin_data/lock if exiting improperly.

To detach without killing the container use Ctrl-p, Ctrl-q.

```
make docker-down
```

For a full docker clean:

```
make docker-clean
```

# TODO #

- [ ] Nodes: Not hardcoded rpcuser/rpcpassword:
- [ ] elements: Show -signblockscript and block.scriptSig
- [ ] elements: Show -fedpegscript
- [ ] Angular: directive for both scriptSig and scriptPubKey
- [ ] e2e Testing: Karma/Protractor/whatever

# License

MIT, see COPYRIGHT.md
