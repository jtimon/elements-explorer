# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import json

from explorer.models.stats import Mempoolstats
from explorer.process.base import CronCacher

MEMPOOL_STATS_INTERVALS = (
    range(1, 5) + range(5, 30, 5) + range(30, 100, 10) +
    range(100, 200, 20) + range(200, 500, 50) + range(500, 1000, 100) + range(1000, 2000, 500))

CURRENCY_UNIT_FLOAT = 100000000

def BtcStrToSatInt(btc_str):
    sat_float = float(btc_str) * CURRENCY_UNIT_FLOAT
    return int(sat_float)

def FeerateFromBtcFeeStrAndVsize(btc_str, vsize):
    fee_sat = BtcStrToSatInt(btc_str)
    return int(fee_sat / vsize)

def IncrementStats(stats, interval, tx_fee, tx_size):
    stats['count'][interval] = stats['count'][interval] + 1
    stats['fee'][interval] = stats['fee'][interval] + BtcStrToSatInt(tx_fee)
    stats['vsize'][interval] = stats['vsize'][interval] + tx_size

class MempoolStatsCacher(CronCacher):

    def __init__(self, chain, rpccaller, db_client, wait_time, initial_wait_time,
                 *args, **kwargs):

        super(MempoolStatsCacher, self).__init__(chain, rpccaller, db_client, wait_time, initial_wait_time,
                                                 *args, **kwargs)

        self.stats_types = ['count', 'fee', 'vsize']
        self.stats_intervals = MEMPOOL_STATS_INTERVALS

    def mempoolstats_insert(self, stat_type, int_time, stats):
        mempoolstats_elem = Mempoolstats(json_dict={
            'time': int_time,
            'stat_type': stat_type,
            'blob': stats[stat_type],
        })

        try:
            mempoolstats_elem.insert()
            print('SUCCESS caching %s in chain %s stat_type %s' % ('mempoolstats', self.chain, stat_type))
        except Exception as e:
            print("Error in MempoolStatsCacher.mempoolstats_insert:", type(e), e)
            print('FAILED caching %s in chain %s %s' % ('mempoolstats', self.chain, json.dumps(mempoolstats_elem.json())))

    def _cron_loop(self):
        mempool_state = self.rpccaller.RpcCall('getrawmempool', {'verbose': True})
        if 'error' in mempool_state and mempool_state['error']:
            return

        stats = {}
        for stats_type in self.stats_types:
            stats[stats_type] = {}
            stats[stats_type]['total'] = 0
            for stats_interval in self.stats_intervals:
                stats[stats_type][stats_interval] = 0

        for txid, tx_entry in mempool_state.iteritems():
            tx_fee = tx_entry['fee']
            tx_size = tx_entry['size']
            tx_feerate = FeerateFromBtcFeeStrAndVsize(tx_fee, tx_size)
            max_interval = self.stats_intervals[-1]

            for stats_interval in self.stats_intervals:
                if tx_feerate <= stats_interval:
                    max_interval = stats_interval

            for stats_interval in self.stats_intervals:
                if tx_feerate <= stats_interval:
                    IncrementStats(stats, stats_interval, tx_fee, tx_size)

            IncrementStats(stats, 'total', tx_fee, tx_size)

        int_time = int((datetime.datetime.now()).strftime('%s'))
        for stat_type in self.stats_types:
            self.mempoolstats_insert(stat_type, int_time, stats)
