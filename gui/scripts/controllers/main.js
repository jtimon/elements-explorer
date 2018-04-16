'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('MainCtrl', function ($scope, $routeParams, $location, SrvUtil, SrvChain, SrvBackend) {

        $scope.curious = $location.search().curious == 'true';
        $scope.loading = true;
        $scope.rawhex_limit = 100;

        function cleanTx() {
            $scope.txid = "";
            $scope.transaction = null;
            $scope.txjson = null;
        }

        function cleanBlockBase() {
            $scope.block = null;
            $scope.blockstats = null;
            $scope.blockjson = null;
        }

        function cleanBlock() {
            cleanBlockBase();
            $scope.blockid = "";
            $scope.blockheight = null;
        }

        cleanTx();
        cleanBlock();

        function successCallbackBlock(data) {
            $scope.block = data;
            $scope.blockid = $scope.block["hash"];
            $scope.blockheight = $scope.block["height"];
            $scope.blockjson = JSON.stringify($scope.block, null, 4);

            return $scope.block["height"];
        };

        function PromBlockstats(height) {
            SrvChain.GetAvailableChains()
                .then(function (available_chains) {
                    if (available_chains[SrvChain.get()]['stats_support']) {
                        return SrvBackend.get("blockstats", height)
                            .then(function(data) {
                                $scope.blockstats = data;
                            });
                    } else {
                        return null;
                    }
                });
        };

        function CreatePromBlockstats(height) {
            return function () {
                return PromBlockstats(height);
            }
        };

        var goToBlock = function(blockhash) {
            return SrvBackend.get("block", blockhash)
                .then(successCallbackBlock)
                .then(PromBlockstats);
        };

        function goToEntry(txhash) {
            return SrvBackend.RpcCall("getmempoolentry", {"txid": txhash})
                .then(function (data) {
                    $scope.mempoolentry = SrvUtil.GetResult(data);
                });
        };

        function successCallbackTx(data) {
            $scope.showtxlist = false;
            $scope.transaction = data;
            $scope.txjson = JSON.stringify($scope.transaction, null, 4);
            if ($scope.transaction["blockhash"]) {
                $scope.blockid = $scope.transaction["blockhash"];
                return goToBlock($scope.blockid);
            } else {
                cleanBlock();
                return goToEntry($scope.transaction['txid']);
            }
        };

        var goToHeight = function(height) {
            return SrvBackend.GetBlockByHeight(height)
                .then(successCallbackBlock)
                .then(CreatePromBlockstats(height))
        };

        var goToTx = function(txhash) {
            return SrvBackend.get("tx", txhash)
                .then(successCallbackTx)
                .catch(SrvUtil.errorCallbackScoped($scope));
            ;
        };

        $scope.IsCTOut = function(output) {
            return !output["value"] && output["value"] != 0;
        };

        $scope.searchBlock = function() {
            cleanBlockBase();
            $scope.blockheight = null;
            if ($scope.blockid == "") {
                cleanBlock();
                return;
            }
            $scope.loading = true;
            cleanTx();
            goToBlock($scope.blockid)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        $scope.searchBlockByHeight = function() {
            $scope.loading = true;
            cleanBlockBase();
            $scope.blockid = "";
            cleanTx();
            goToHeight($scope.blockheight)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        };
        $scope.prevHeight = function() {
            $scope.blockheight = $scope.blockheight - 1;
            $scope.searchBlockByHeight();
        };
        $scope.nextHeight = function() {
            $scope.blockheight = $scope.blockheight + 1;
            $scope.searchBlockByHeight();
        };

        $scope.searchTx = function() {
            if ($scope.txid == "") {
                cleanTx();
                return;
            }
            $scope.loading = true;
            cleanBlock();
            goToTx($scope.txid)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        var EXAMPLE_LIST_SIZE = 4;

        function LoadMempoolTxs()
        {
            return SrvBackend.RpcCall("getrawmempool", {})
                .then(function(data) {
                    $scope.mempooltxs = SrvUtil.GetResult(data).slice(0, EXAMPLE_LIST_SIZE);
                });
        };

        function ProcessBlock(block) {
            $scope.recentblocks.push({
                'height': block['height'],
                'mediantime': block['mediantime'],
                'size': block['size'],
                'tx_count': block['tx'].length,
                'hash': block['hash']
            });
            if (block.hasOwnProperty('previousblockhash')) {
                return block['previousblockhash'];
            }
            return null;
        }

        function LoadBlocksAndConfirmedTxs()
        {
            return SrvChain.GetChainInfo()
                .then(function(chaininfo) {
                    $scope.recentblocks = [];
                    var promise = SrvBackend.get("block", chaininfo['bestblockhash'])
                        .then(function(block) {
                            $scope.confirmed_txs = block['tx'].slice(0, EXAMPLE_LIST_SIZE);
                            return block;
                        })
                        .then(ProcessBlock);

                    for (var i = 0; i < EXAMPLE_LIST_SIZE - 1; i++) {
                        promise = promise.then(function (blockhash) {
                            if (blockhash) {
                                return SrvBackend.get("block", blockhash).then(ProcessBlock);
                            }
                            return null;
                        });
                    }
                    return promise;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        function NothingSelectedLoad()
        {
            $scope.loading = true;
            LoadBlocksAndConfirmedTxs()
                .then(LoadMempoolTxs)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        function DoMain()
        {
            if ($routeParams.block) {
                $scope.blockid = $routeParams.block;
                goToBlock($routeParams.block)
                    .then(function() {
                        $scope.loading = false;
                    })
                    .catch(SrvUtil.errorCallbackScoped($scope));
            } else if ($routeParams.block_height) {
                $scope.blockheight = parseInt($routeParams.block_height);
                $scope.searchBlockByHeight()
            } else if ($routeParams.txid) {
                $scope.txid = $routeParams.txid;
                goToTx($routeParams.txid)
                    .then(function() {
                        $scope.loading = false;
                    })
                    .catch(SrvUtil.errorCallbackScoped($scope));
            } else {
                NothingSelectedLoad();
            }
        }

        SrvChain.set()
            .then(function (selected_chain) {
                $scope.parent_chain = SrvChain.GetParentChain();
            })
            .then(DoMain)
            .catch(SrvUtil.errorCallbackScoped($scope));
    });
