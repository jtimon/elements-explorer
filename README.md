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
make
```

or 

```
make dev
```

Visit the local web going to http://127.0.0.1:5000

If you prefer it to be run as a daemon use:

```
make staging
```

or 

```
make production
```

## Closing ##

If you're running dev, just Ctrl-c.
If You're running staging or production:


```
make stop
```

For a full docker clean:

```
make clean
```

## Starting and restating the DB ##

For starting and restating the database, the create_db process in
https://github.com/jtimon/rpc-explorer/blob/master/docker/explorer/Procfile
must be active. Conversely, to stop the db from being restarted with
every deployment/run, one must comment that line/process of the Procfile.

Currently the db needs to be restarted whenever:

- The schema changes in any way.
- Some of the data stored in blob fields changes
- The reorg handling code shows to be faulty
- Any daemon witnessed a 100-block reorg
- Any daemon crashed or got into a bad state that justifies restarting
  its persistent cache


## greedy caching ##

As explained in the previous section, processes can be activated or
deactivated in https://github.com/jtimon/rpc-explorer/blob/master/docker/explorer/Procfile .

One of the processes one may want to run when the db is not being
restarted is the greedy cacher for any selected set of chains.

It will slow down initialization and in general everything until it
runs down to height 0 for its chain from the first successfully
getchaininfo result at least once. After that, if the reorg handling
processes are activated, it just double checks that blocks are cached
at least once. Greedy cachers are independent from reorg handling
processes, and thus what they cache may be deleted.

Since they are very noisy, they are only recommended when you want to
fill the db cache but you don't want to see extra messages in your
logs. Deactivating them should be always fine.

On anything resembling production, they should be activated too, even
if they take days to fill the db cache the first time, since any
response coming the db without bothering the daemon is one chance less
for a denial of service attack, which, by the way, the whole project
is exposed to even after that unless you're working on a closed
network where you can take care of those attacks in some other way or
if you're just using this project as a developer as you should. In
that latter case you just have to remember not to DoS yourself harder
than your machine can take, but please send back any weird concurrency
errors you get.

# TODO #

- [ ] Nodes: Not hardcoded rpcuser/rpcpassword:
- [ ] elements: Show -signblockscript and block.scriptSig
- [ ] elements: Show -fedpegscript
- [ ] Angular: directive for both scriptSig and scriptPubKey
- [ ] e2e Testing: Karma/Protractor/whatever

# License

MIT, see COPYING
