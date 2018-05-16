'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvBackend', function SrvBackend($q, $http, SrvChain, SrvUtil) {

        var BACKEND_URL = '/api/v0';
        var srv = {};
        var cache = {};

        srv.RpcCall = function(rpcMethod, vRpcParams) {
            vRpcParams['chain'] = SrvChain.get();
            return $http.post(BACKEND_URL + '/' + rpcMethod, vRpcParams);
        };

        function CacheBlockResponse(chain)
        {
            return function (response) {
                var block = GetResult(response);
                block['tx'] = JSON.parse(block['tx']);
                cache[chain]['block'][ block['id'] ] = block;
                cache[chain]['blockheight'][ block['height'] ] = block['id'];
                return block;
            }
        };

        srv.get = function(resource, id) {
            var chain = SrvChain.get();
            SrvUtil.PreCache(cache, chain, resource);

            var retPromise;
            if (cache[chain][resource][id]) {
                retPromise = $q(function(resolve) {
                    resolve(cache[chain][resource][id]);
                });
            } else {
                if (resource == 'block') {
                    SrvUtil.PreCache(cache, chain, 'blockheight');
                    retPromise = srv.RpcCall(resource, {'id': id})
                        .then(CacheBlockResponse(chain));
                } else {
                    retPromise = srv.RpcCall(resource, {'id': id})
                        .then(SrvUtil.CacheElem(cache, chain, resource, id));
                }

            }
            return retPromise;
        };

        srv.GetBlockByHeight = function(height) {
            var chain = SrvChain.get();
            SrvUtil.PreCache(cache, chain, 'blockheight');
            SrvUtil.PreCache(cache, chain, 'block');

            var retPromise;
            if (cache[chain]['blockheight'][height]) {
                retPromise = $q(function(resolve) {
                    var blockhash = cache[chain]['blockheight'][height];
                    resolve(cache[chain]['block'][blockhash]);
                });
            } else {
                retPromise = srv.RpcCall('blockheight', {'id': height})
                    .then(CacheBlockResponse(chain));
            }
            return retPromise;
        };

        var MAX_PARALLEL_IT = 500;

        srv.GetBlockStats = function(start, end) {
            var chain = SrvChain.get();
            var resource = 'blockstats';
            SrvUtil.PreCache(cache, chain, resource);

            var promises = [];
            var it_parallel = 0;

            for (var i = start; i <= end; i++) {
                if (!cache[chain][resource][i]) {
                    function task(index) {
                        return function task_func() {
                            return srv.RpcCall(resource, {"id": index});
                        }
                    }
                    if (!promises[it_parallel]) {
                        promises[it_parallel] = task(i)();
                    } else {
                        promises[it_parallel] = promises[it_parallel].then(task(i));
                    }
                    promises[it_parallel] = promises[it_parallel].then(SrvUtil.CacheElem(cache, chain, resource, i));
                    if (it_parallel == MAX_PARALLEL_IT - 1) {
                        it_parallel = 0;
                    } else {
                        ++it_parallel;
                    }
                }
            }

            function AccumulateStats(){
                var formatted_data = {};
                for (var it_height = start; it_height <= end; it_height++) {
                    var result = cache[chain][resource][it_height];
                    if (result) {
                        for (var key in result) {
                            if (result.hasOwnProperty(key)) {
                                if (!formatted_data[key]) {
                                    formatted_data[key] = [];
                                }
                                formatted_data[key].push(result[key]);
                            }
                        }
                    }
                }
                return formatted_data;
            }

            var retPromise;
            if (promises.length > 0) {
                retPromise = $q.all(promises).then(AccumulateStats);
            } else {
                retPromise = $q(function(resolve) {
                    resolve(AccumulateStats());
                });
            }
            return retPromise;
        };

        return srv;
    })
