# Elements explorer

A simple block explorer based on deamon's rpc calls.
It supports https://github.com/ElementsProject/elements and should be
easy to adapt to support other chains based on the elements codebase.

# Installation: #

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

Also, an 'explorer-data' directory needs to exist alongside the
project dir for it to work.

From inside the cloned directory:

```
mkdir ../explorer-data
```

# Build & development #

There are several targets on the makefile, some are generic, but most
depend on the environment.

There are 3 supported environments:

```
dev
staging
production
```

All of them have their own configuration directory in ./docker.
All of them have two ways of being run: '<env>' and '<env>'-nod.

For example, one can do:

```
make dev
<do stuff>
make stop-dev
```
(In this case '<env>'=dev)

Or one can also do:

```
make dev-nod
<do stuff>
Ctrl-c
```
(In this case '<env>'=dev)

The first one will run the explorer as daemon in the background and
one has to stop it manually and differently for each env in the
following way:

```
make stop-'<env>'
```

The second form including "-nod" stand for "no daemon", meaning you
will see the logs in your terminal directly without accessing the
containers logs directly and one can also stop with Ctrl-c instead of
having to remember which env is to stop.

For those who want to see the logs withour using the "-nod" targets,
here are some variations:

```
sudo docker logs -f rpcexplorer_explorer_1
sudo docker logs rpcexplorer_daemons_1
sudo docker logs rpcexplorer_postgres_1
```

For all the supported environments, there's an ipython-'<env>', so that
one can go into REPL with all the dependencies installed and the db
and daemons running within docker without having to install and
reproduce anything locally. For example:

```
make ipython-dev
```

# Testing #

Currently most of the testing is done manually.
There are tools for automatic testing of the python parts now, and
some tests, but not many, in https://github.com/jtimon/elements-explorer/tree/master/explorer/tests .

## Testing basics ##

One can run all the supported tests with:

```
make check-all
```

...or...


```
python3 ./run_tests.py --dbs=dummydb,postgres
```

...are currently equivalent.


That will run the tests through all the supported databases, currently:

```
dummydb
postgres
```

## Advanced testing ##

If one wants to run all tests for a given database:

```
make check-<db>
```

...or...


```
python3 ./run_tests.py --dbs=<db>
```

...are currently equivalent.

One can also run individual tests or groups of tests for a given db or
group of dbs. There's some examples below:

```
python3 ./run_tests.py --dbs=dummydb
python3 ./run_tests.py --dbs=postgres
python3 ./run_tests.py --tests=api_faucet.py
python3 ./run_tests.py --tests=process_generator.py
python3 ./run_tests.py --dbs=dummydb,postgres --tests=api_faucet.py
python3 ./run_tests.py --dbs=dummydb,postgres --tests=api_faucet.py,process_generator.py
python3 ./run_tests.py --dbs=dummydb --tests=api_faucet.py
python3 ./run_tests.py --dbs=dummydb --tests=api_faucet.py,process_generator.py
python3 ./run_tests.py --dbs=postgres --tests=api_faucet.py
python3 ./run_tests.py --dbs=postgres --tests=api_faucet.py,process_generator.py
python3 ./run_tests.py --dbs=dummydb,postgres --tests=api_faucet.py
python3 ./run_tests.py --dbs=dummydb,postgres --tests=api_faucet.py,process_generator.py
```

## Starting and restating the DB ##

For starting and restating the database, the create_db process in
https://github.com/jtimon/elements-explorer/blob/master/docker/explorer/Procfile
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
deactivated in https://github.com/jtimon/elements-explorer/blob/master/docker/explorer/Procfile .

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

# License

MIT, see COPYING
