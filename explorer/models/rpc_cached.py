# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from mintools.ormin.model import CachedModel

class RpcCachedModel(CachedModel):

    @classmethod
    def set_rpccaller(cls, value):
        cls._rpccaller = value
