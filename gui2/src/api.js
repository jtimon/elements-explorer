function apiChainInfo() {
  const url = 'http://localhost:5000/api/v0/chaininfo';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      chain: 'testnet3',
      id: 'testnet3',
    }),
  };
  return fetch(url, requestParams)
    .then(response => response.json())
    .then(data => data);
}

function apiGetBlockByHash(id) {
  const url = 'http://localhost:5000/api/v0/block';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      id,
      chain: 'testnet3',
    }),
  };
  return fetch(url, requestParams)
    .then(response => response.json())
    .then(data => data);
}

function apiGetBlockByHeight(id) {
  const url = 'http://localhost:5000/api/v0/blockheight';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      id,
      chain: 'testnet3',
    }),
  };
  return fetch(url, requestParams)
    .then(response => response.json())
    .then(data => data);
}

function apiGetBlockStats(id) {
  const url = 'http://localhost:5000/api/v0/blockstats';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      id,
      chain: 'testnet3',
    }),
  };
  return fetch(url, requestParams)
    .then(response => response.json())
    .then(data => data);
}

function apiGetTransaction(id) {
  const url = 'http://localhost:5000/api/v0/tx';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      id,
      chain: 'testnet3',
    }),
  };
  return fetch(url, requestParams)
    .then(response => response.json())
    .then(data => data);
}

module.exports = {
  apiChainInfo,
  apiGetBlockByHash,
  apiGetBlockByHeight,
  apiGetBlockStats,
  apiGetTransaction,
};
