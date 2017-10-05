#!/usr/bin/env python
if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import gflags

gflags.DEFINE_string('address', u"localhost:1984", 
                     u"Address clients will connect to")

gflags.DEFINE_string('proxyaddress', u"2000", u"")

gflags.DEFINE_string('dbaddress', u"localhost:1984",
    u"Network address backend database")

gflags.DEFINE_string('dbtype', u"dummy",
    u"Backend type for MinQL server")

gflags.DEFINE_integer('workers', 10,
    u"Number of proxy Workers",
    short_name='w')
gflags.RegisterValidator('workers',
    lambda workers: 1 <= workers <= 50,
    message=u"Number of workers must be between 1 and 50.")

gflags.DEFINE_string('schema', u"",
    u"Schema for MinQL server")

gflags.DEFINE_string('dataset', u"",
    u"Dataset for MinQL server")

try:
    import sys
    argv = gflags.FLAGS(sys.argv)
except gflags.FlagsError, e:
    print('%s\n\nUsage %s ARGS \n%s' % (e, sys.argv[0], gflags.FLAGS))
    sys.exit(0)
FLAGS = gflags.FLAGS

# ===----------------------------------------------------------------------===

from lib import zmqmin
from lib import minql

import time
time.sleep(1)

if FLAGS.workers > 1:
    single=False
    address=FLAGS.proxyaddress
else:
    single=True
    address=FLAGS.address

# FIX flags.w = 1 case, flags -> params mapping wrong
for server_id in range(FLAGS.workers):
    ddb = minql.ZmqMinqlServer(
        FLAGS.dbtype, 
        single=single, 
        address=address,
        db_address=FLAGS.dbaddress,
        worker_id='ZmqServer_%s' % server_id)
    ddb.start()

if not single:
    request_queue = zmqmin.Queue(FLAGS.address, FLAGS.proxyaddress)
    request_queue.start()

if FLAGS.schema:
    c = minql.MinqlClient('zmq', FLAGS.address)
    c.put_schema_from_file(FLAGS.schema)
    if FLAGS.dataset:
        c.put_dataset_from_file(FLAGS.dataset)
