'use strict';
/*global $:false */

function NumToPositive(num) {
    return (num > 0) ? (num) : 0;
}

function NumToNatural(num) {
    return (num > 1) ? (num) : 1;
}

function ParseIntToPositive(num) {
    return NumToPositive(parseInt(num));
}

function ParseNatural(num) {
    return NumToNatural(parseInt(num));
}

function GetResult(response) {
    if (response['data']['result']) {
        // TODO remove spacial case for getrawmempool
        return response['data']['result'];
    } else {
        return response['data'];
    }
}

function errorCallbackScoped(myscope)
{
    return function (data) {
        if (typeof data === 'string') {
            myscope.error = data;
        } else if (data["data"] && data["data"]["error"]) {
            myscope.error = data["data"]["error"];
        } else {
            myscope.error = JSON.stringify(data, null, 4);
        }
    };
}

function PreCache(cache, chain, resource) {
    if (!cache[chain]) {
        cache[chain] = {};
    }
    if (!cache[chain][resource]) {
        cache[chain][resource] = {};
    }
}

function CacheResult(cache, chain, resource, id) {
    function cache_callback(result) {
        cache[chain][resource][id] = result;
        return cache[chain][resource][id];
    }
    return cache_callback;
}

function CacheElem(cache, chain, resource, id) {
    function cache_callback(response) {
        var result = GetResult(response);
        return CacheResult(cache, chain, resource, id)(result);
    }
    return cache_callback;
}

function GetKeys(dictionary)
{
    var keys = [];
    for (var key in dictionary) {
        if (dictionary.hasOwnProperty(key)) {
            keys.push(key);
        }
    }
    return keys;
}

angular.module('rpcExplorerApp')
    .service('SrvUtil', function SrvUtil() {

        var srv = {};
        srv.errorCallbackScoped = errorCallbackScoped;
        srv.PreCache = PreCache;
        srv.CacheElem = CacheElem;
        srv.CacheResult = CacheResult;
        srv.GetResult = GetResult;
        srv.NumToPositive = NumToPositive;
        srv.ParseIntToPositive = ParseIntToPositive;
        srv.ParseNatural = ParseNatural;
        srv.GetKeys = GetKeys;
        return srv;
    });
