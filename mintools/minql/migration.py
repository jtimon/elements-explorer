# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import json

def get_table_migration_scheme(new_scheme, old_scheme):
    diff = {}
    deleted_fields = [nf for nf in old_scheme.keys() if nf not in new_scheme.keys() ]
    if deleted_fields:
        diff['drop_column'] = deleted_fields

    new_fields = [nf for nf in new_scheme.keys() if nf not in old_scheme.keys() ]
    if new_fields:
        diff['add_column'] = {}
        for f_name in new_fields:
            diff['add_column'][f_name] = new_scheme[f_name]

    for field, f_properties in new_scheme.iteritems():
        if field in new_fields:
            continue
        old_properties = old_scheme[field]
        a, b = json.dumps(f_properties, sort_keys=True), json.dumps(old_properties, sort_keys=True)
        if a != b:
            if not 'modify_column' in diff:
                diff['modify_column'] = {}
            diff['modify_column'][field] = {
                'new': f_properties,
                'old': old_properties,
            }

    return diff


def get_migration_schema(new_schema, old_schema):

    to_create = {}
    alter_schema = {}
    for table, new_scheme in new_schema.iteritems():
        if not table in old_schema:
            to_create[table] = new_scheme
        else:
            old_scheme = old_schema[table]
            table_alter_scheme = get_table_migration_scheme(new_scheme, old_scheme)
            if table_alter_scheme:
                alter_schema[table] = table_alter_scheme

    migration_diff = {}
    if to_create:
        migration_diff['create'] = to_create

    if alter_schema:
        migration_diff['alter'] = alter_schema

    to_drop = list(set(old_schema.keys()) - set(new_schema.keys()))
    if to_drop:
        migration_diff['drop'] = to_drop

    print('migration_diff', migration_diff)
    return migration_diff

class Migration(object):

    def __init__(self, client, schema, *args, **kwargs):

        self.client = client
        self.schema = schema

        super(Migration, self).__init__(*args, **kwargs)

    def migrate(to_client=None, to_schema=None):

        if to_client:

            if not to_schema:
                migrate_basic(to_client)
            else:
                migrate_changes(to_client, to_schema)

        elif to_schema:

            from .impl.dummy.client import DummyMinqlClient
            middle_client = DummyMinqlClient(url, port)
            self.migrate_basic(middle_client)
            aux_mig = Migration(middle_client, self.schema)
            aux_mig.migrate_changes(self.client, to_schema)

    def migrate_basic(self, to_schema):

        for table_name, s in schema.iteritems():

            try:
                to_client.drop_table(table_name)
            except TableNotFoundError:
                pass
            to_client.create_table(table_name, s)

            rows = self.client.search(table_name)
            for row in rows:
                self.client.put(table_name, row)

    def migrate_changes(self, to_client, to_schema):

        raise NotImplementedError
