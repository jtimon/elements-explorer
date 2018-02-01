#!/usr/bin/env python
if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import gflags

gflags.DEFINE_string('address', u"localhost:1984", 
                     u"Address clients will connect to")

gflags.DEFINE_string('dbaddress', u"localhost:1984",
    u"Network address backend database")

gflags.DEFINE_string('dbtype', u"dummy",
    u"Backend type for MinQL server")

gflags.DEFINE_string('dbname', u"dbname",
    u"Backend db name for MinQL server")

gflags.DEFINE_string('dbuser', u"dbuser",
    u"Backend db user for MinQL server")

gflags.DEFINE_string('dbpass', u"dbpass",
    u"Backend db password for MinQL server")

gflags.DEFINE_string('schema', u"",
    u"Schema for MinQL server")

gflags.DEFINE_string('dataset', u"",
    u"Dataset for MinQL server")

gflags.DEFINE_string('chains', u"bitcoin,testnet3,elementsregtest",
    u"Chains to restart the db for")

try:
    import sys
    argv = gflags.FLAGS(sys.argv)
except gflags.FlagsError, e:
    print('%s\n\nUsage %s ARGS \n%s' % (e, sys.argv[0], gflags.FLAGS))
    sys.exit(0)
FLAGS = gflags.FLAGS

# ===----------------------------------------------------------------------===

from mintools import zmqmin
from lib import minql

import time
time.sleep(1)

ddb = minql.ZmqMinqlServer(
    FLAGS.dbtype, 
    single=True, 
    address=FLAGS.address,
    db_address=FLAGS.dbaddress,
    db_name=FLAGS.dbname,
    db_user=FLAGS.dbuser,
    db_pass=FLAGS.dbpass,
    worker_id='ZmqServer')
ddb.start()

CHAINS = FLAGS.chains.split(',')

if FLAGS.schema:
    schema = minql.read_json(FLAGS.schema)
    per_chain_schema = {}
    for table_name in schema:
        table_schema = schema[table_name]
        for chain in CHAINS:
            per_chain_schema[chain + "_" + table_name] = table_schema

    c = minql.MinqlClientFactory('zmq')(FLAGS.address)
    c.put_schema(per_chain_schema)
    if FLAGS.dataset:
        c.put_dataset_from_file(FLAGS.dataset)
