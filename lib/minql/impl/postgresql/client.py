
import psycopg2
import psycopg2.extras

from ..sql import SqlMinqlClient

class PostgresqlMinqlClient(SqlMinqlClient):

    def __init__(self, address, name, user, password, *args, **kwargs):

        url, port = address.split(':')
        params = "dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (name, user, password, url, port)
        self.connection = psycopg2.connect(params)

        super(PostgresqlMinqlClient, self).__init__(*args, **kwargs)

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
        print 'Creating PostgreSQL table %s' % table_name

        attrs = []
        for key, value in schema.iteritems():

            attr = '"%s" ' % key
            if value['type'] == 'string':
                attr += 'VARCHAR(500)'
            elif value['type'] == 'float':
                attr += 'REAL'
            elif value['type'] == 'int':
                attr += 'INT'
            elif value['type'] == 'text':
                attr += 'TEXT'
            else:
                raise NotImplementedError
            
            if value['required']:
                attr += ' NOT NULL'

            attrs.append(attr)

        table = '''
        CREATE TABLE "%s" (
            id VARCHAR(100) PRIMARY KEY NOT NULL''' % table_name
        if attrs:
            table += ', \n' + ', \n'.join(attrs)
        table += ');'

        cur = self.connection.cursor()
        print table
        cur.execute(table)
        self.connection.commit()

        for key, value in schema.iteritems():

            if 'index' in value and value['index']:
                index = 'CREATE INDEX "%s_%s_index" ON "%s" ("%s");' % (
                    table_name, key, table_name, key)
                cur = self.connection.cursor()
                print index
                cur.execute(index)
                self.connection.commit()

    # TODO postgres doesn't drop tables
    def _drop_table(self, table_name):
        print 'postgres drop table', table_name
        cur = self.connection.cursor()
        self.connection.set_isolation_level(0)
        cur.execute('DROP TABLE IF EXISTS "%s"' % table_name)
        # cur.execute('ALTER TABLE "%s" DROP CONSTRAINT  "%s"' % (
        #     table_name, table_name))
        # cur.execute('DROP DATABASE IF EXISTS "%s"' % table_name)
        # print 'DROP DATABASE IF EXISTS "%s"' % table_name
        # self.connection.commit()

    def search(self, table_name, criteria={}):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'SELECT * from "%s"' % table_name

        if criteria:

            crit = []
            for attr, value in criteria.iteritems():

                if type(value) is dict:
                    # TODO replace 'ge' with '>=' everywhere 
                    if 'ge' in value:
                        criterion = '%s >= %s' % (attr, str(value['ge']))
                    if 'le' in value:
                        criterion = '%s <= %s' % (attr, str(value['le']))
                elif isinstance(value, basestring):
                    criterion = "%s = '%s'" % (attr, value)
                else:
                    criterion = '%s = %s' % (attr, str(value))
                crit.append(criterion)
            query += ' where ' + ' and '.join(crit)

        cur.execute(query)
        return cur.fetchall()

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
        query = 'UPDATE "%s" SET %s' % (
            table_name, ', '.join(updates))
        query += " where id = '%s'" % row['id']

        cur.execute(query)
        self.connection.commit()
        return row

    def insert(self, table_name, row):
        cur = self.connection.cursor()

        values = []
        for value in row.values():
            if isinstance(value, basestring):
                values.append( "'%s'" % value )
            else:
                values.append( str(value) )

        query = 'INSERT INTO "%s" (%s) VALUES (%s)' % (
            table_name, 
            ', '.join(row.keys()), 
            ', '.join(values)
        )
        print query
        cur.execute(query)
        self.connection.commit()
        return row

    def _get(self, table_name, id):
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'SELECT * from "%s"' % table_name
        query += " where id = '%s'" % id
        print query
        cur.execute(query)
        return cur.fetchone()
