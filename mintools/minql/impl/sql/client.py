# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from ...interface import MinqlBaseClient

class SqlMinqlClient(MinqlBaseClient):

    def update(self, table_name, row):
        raise NotImplementedError

    def insert(self, table_name, row):
        raise NotImplementedError

    def put(self, table_name, row):

        if self._get(table_name, row['id']):
            return self.update(table_name, row)
        return self.insert(table_name, row)
