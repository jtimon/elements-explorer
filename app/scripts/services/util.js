'use strict';
/*global $:false */

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

angular.module('rpcExplorerApp')
    .service('SrvUtil', function SrvUtil() {

        var srv = {};
        srv.errorCallbackScoped = errorCallbackScoped;
        srv.PreCache = PreCache;
        return srv;
    });
