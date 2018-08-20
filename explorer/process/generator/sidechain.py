# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from explorer.process.base import CronCacher

class SidechainGenerator(CronCacher):

    def __init__(self, chain, rpccaller, parent_rpccaller, wait_time, initial_wait_time,
                 *args, **kwargs):

        self.parent_rpccaller = parent_rpccaller

        super(SidechainGenerator, self).__init__(chain, rpccaller, None, wait_time, initial_wait_time,
                                                 *args, **kwargs)
