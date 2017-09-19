'use strict';
/*global $:false */

function GetResult(response) {
    return response['data']['result'];
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

function CacheElem(cache, chain, resource, id) {
    function cache_callback(response) {
        cache[chain][resource][id] = GetResult(response);
        return cache[chain][resource][id];
    }
    return cache_callback;
}

angular.module('rpcExplorerApp')
    .service('SrvUtil', function SrvUtil() {

        var srv = {};
        srv.errorCallbackScoped = errorCallbackScoped;
        srv.PreCache = PreCache;
        srv.CacheElem = CacheElem;
        srv.GetResult = GetResult;
        return srv;
    });
