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

gflags.DEFINE_string('model', u"",
    u"Ormin model to translate to MinQL schema")

gflags.DEFINE_string('modelschema', u"",
    u"Target MinQL schema file path to import/export the ormin model")

gflags.DEFINE_string('dataset', u"",
    u"Dataset for MinQL server")

gflags.DEFINE_string('chains', u"bitcoin,testnet3,elementsregtest",
    u"Chains to restart the db for")

gflags.DEFINE_string('forcechains', u"",
    u"Chains to restart the db for")

gflags.DEFINE_string('forcetables', u"",
    u"Tables to restart the db for")

try:
    import sys
    argv = gflags.FLAGS(sys.argv)
except gflags.FlagsError, e:
    print('%s\n\nUsage %s ARGS \n%s' % (e, sys.argv[0], gflags.FLAGS))
    sys.exit(0)
FLAGS = gflags.FLAGS

# ===----------------------------------------------------------------------===

import json

from mintools.minql import (
    MinqlClientFactory,
    ZmqMinqlServer,
    get_migration_schema,
    write_json,
)

import time
time.sleep(1)

migration_schema = {}
migration_diff = {}
CHAINS = FLAGS.chains.split(',')

FORCE_CHAINS = FLAGS.forcechains.split(',')
if len(FORCE_CHAINS) == 1 and FORCE_CHAINS[0] == '':
    FORCE_CHAINS = []

FORCE_TABLES = FLAGS.forcetables.split(',')
print('FORCE_TABLES', FORCE_TABLES)
if len(FORCE_TABLES) == 1 and FORCE_TABLES[0] == '':
    FORCE_TABLES = []

ddb = ZmqMinqlServer(
    FLAGS.dbtype,
    single=True,
    address=FLAGS.address,
    db_address=FLAGS.dbaddress,
    db_name=FLAGS.dbname,
    db_user=FLAGS.dbuser,
    db_pass=FLAGS.dbpass,
    worker_id='ZmqServer')
ddb.start()

db_client = MinqlClientFactory('zmq')(FLAGS.address)

if FLAGS.model and FLAGS.modelschema:
    try:
        old_file = open(FLAGS.modelschema, 'r').read()
        old_schema = json.loads(old_file)
        print('old_schema', old_schema)
        write_json(FLAGS.modelschema + '.old.json', old_schema)
    except IOError:
        old_schema = None

    import imp
    model_module = imp.load_source('model', FLAGS.model)
    print('Exporting the following schema to %s ...' % (FLAGS.modelschema))
    new_schema = model_module.ORMIN_DOMAIN.json_schema()
    print('new_schema', new_schema)
    write_json(FLAGS.modelschema, new_schema)

    if old_schema:
        migration_diff = get_migration_schema(new_schema, old_schema)
        write_json(FLAGS.modelschema + '.migration_diff.json', migration_diff)

        if 'drop' in migration_diff:
            for table_name in migration_diff['drop']:
                for chain in CHAINS:
                    db_client.drop_table(chain + "_" + table_name)

        if 'create' in migration_diff:
            migration_schema = migration_diff['create']

        # For now just restart all tables that need to be altered
        if 'alter' in migration_diff:
            for table_name in migration_diff['alter']:
                migration_schema[table_name] = new_schema[table_name]
    else:
        migration_schema = new_schema

print('migration_schema', migration_schema)
if migration_schema:
    write_json(FLAGS.modelschema + '.last_migration.json', migration_schema)

    per_chain_schema = {}
    for table_name in migration_schema:
        for chain in CHAINS:
            per_chain_schema[chain + "_" + table_name] = migration_schema[table_name]

    db_client.put_schema(per_chain_schema)

if FORCE_CHAINS:
    forced_chains_schema = {}
    for table_name in new_schema:
        for chain in FORCE_CHAINS:
            forced_chains_schema[chain + "_" + table_name] = new_schema[table_name]

    print('forced_chains_schema', forced_chains_schema)
    db_client.put_schema(forced_chains_schema)

if FORCE_TABLES:
    print('FORCE_TABLES', FORCE_TABLES)
    force_tables_schema = {}
    for table_name in FORCE_TABLES:
        assert(table_name in new_schema)
        print('table_name', 'new_schema', table_name, new_schema)
        for chain in CHAINS:
            force_tables_schema[chain + "_" + table_name] = new_schema[table_name]

    print('force_tables_schema', force_tables_schema)
    db_client.put_schema(force_tables_schema)

if FLAGS.dataset:
    db_client.put_dataset_from_file(FLAGS.dataset)

# Force printing after completing (the process will keep running with ddb)
raise NotImplementedError
