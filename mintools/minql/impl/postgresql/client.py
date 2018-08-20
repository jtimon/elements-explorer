# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import psycopg2
import psycopg2.extras

from ..sql import SqlMinqlClient

class PostgresqlMinqlClient(SqlMinqlClient):

    def __init__(self, address, name, user, password, *args, **kwargs):

        url, port = address.split(':')
        params = "dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (name, user, password, url, port)
        self.connection = psycopg2.connect(params)
        self.print_values_query = False

        super(PostgresqlMinqlClient, self).__init__(*args, **kwargs)

    def try_commit(self):
        try:
            self.connection.commit()
        except psycopg2.Error as e:
            print("Error in PostgresqlMinqlClient.try_commit:", {
                'message': e.pgerror,
                'type': type(e),
                'code': e.pgcode,
                'full': e,
            })
            raise e

    # TODO find out how to do the same in hyperdex
    # and add it to the interface?
    def get_tables():
        cur = self.connection.cursor()
        cur.execute("""SELECT datname from pg_database""")
        rows = cur.fetchall()
        tables = []
        for row in rows:
            tables.append(row[0])
        return tables

    def create_table(self, table_name, schema):
        print('Creating PostgreSQL table %s' % table_name)

        attrs = []
        for key, value in schema.iteritems():

            attr = '"%s" ' % key
            if value['type'] == 'string':
                attr += 'VARCHAR(500)'
            elif value['type'] == 'float':
                attr += 'REAL'
            elif value['type'] == 'int':
                attr += 'INT'
            elif value['type'] == 'bigint':
                attr += 'BIGINT'
            elif value['type'] == 'text':
                attr += 'TEXT'
            else:
                raise NotImplementedError

            if value['required']:
                attr += ' NOT NULL'

            attrs.append(attr)

        query = '''
        CREATE TABLE "%s" (
            id VARCHAR(100) PRIMARY KEY NOT NULL''' % table_name
        if attrs:
            query += ', \n' + ', \n'.join(attrs)
        query += ');'

        cur = self.connection.cursor()
        print(query)
        cur.execute(query)
        self.try_commit()

        for key, value in schema.iteritems():

            if 'index' in value and value['index']:
                query = 'CREATE INDEX "%s_%s_index" ON "%s" ("%s");' % (
                    table_name, key, table_name, key)
                print(query)
                cur = self.connection.cursor()
                cur.execute(query)
                self.try_commit()

    # TODO postgres doesn't drop tables
    def _drop_table(self, table_name):
        print('postgres drop table', table_name)
        query = 'DROP TABLE IF EXISTS "%s"' % table_name
        print(query)
        cur = self.connection.cursor()
        self.connection.set_isolation_level(0)
        # cur.execute('ALTER TABLE "%s" DROP CONSTRAINT  "%s"' % (
        #     table_name, table_name))
        cur.execute(query)
        self.try_commit()

    def get_criteria_string(self, criteria):
         if criteria:
            crit = []
            for attr, value in criteria.iteritems():

                if type(value) is dict:
                    # TODO replace 'ge' with '>=' everywhere
                    if 'ge' in value:
                        criterion = '%s >= %s' % (attr, str(value['ge']))
                    if 'le' in value:
                        criterion = '%s <= %s' % (attr, str(value['le']))
                    if 'gt' in value:
                        criterion = '%s > %s' % (attr, str(value['gt']))
                    if 'lt' in value:
                        criterion = '%s < %s' % (attr, str(value['lt']))
                elif isinstance(value, basestring):
                    criterion = "%s = '%s'" % (attr, value)
                else:
                    criterion = '%s = %s' % (attr, str(value))
                crit.append(criterion)
            return ' where ' + ' and '.join(crit)
         else:
             return ''

    def search(self, table_name, criteria={}):
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'SELECT * from "%s"' % table_name
        query += self.get_criteria_string(criteria)

        print(query)
        cur.execute(query)
        return cur.fetchall()

    def delete(self, table_name, criteria):
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'DELETE FROM "%s"' % table_name
        query += self.get_criteria_string(criteria)

        print(query)
        cur.execute(query)

    def update(self, table_name, row):
        assert 'id' in row and row['id'], 'The row needs an id field.'

        cur = self.connection.cursor()

        updates = []
        for key, value in row.iteritems():
            if key != 'id':
                if isinstance(value, basestring):
                    val = "'%s'" % value
                else:
                    val = str(value)
                updates.append('%s = %s' % (key, val) )
        prequery = 'UPDATE "%s"' % table_name
        query = '%s SET %s' % (
            prequery, ', '.join(updates))
        postquery = " where id = '%s'" % row['id']
        query += postquery
        if self.print_values_query:
            print(query)
        else:
            print(prequery, postquery)

        cur.execute(query)
        self.try_commit()
        return row

    def insert(self, table_name, row):
        cur = self.connection.cursor()

        values = []
        for value in row.values():
            if isinstance(value, basestring):
                values.append( "'%s'" % value )
            else:
                values.append( str(value) )

        query = 'INSERT INTO "%s" (%s)' % (
            table_name,
            ', '.join(row.keys()),
        )
        print(query)
        query = '%s VALUES (%s)' % (
            query,
            ', '.join(values)
        )
        if self.print_values_query:
            print(query)

        cur.execute(query)
        self.try_commit()
        return row

    def _get(self, table_name, id):
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'SELECT * from "%s"' % table_name
        query += " where id = '%s'" % id
        print(query)
        cur.execute(query)
        return cur.fetchone()
