function getChainInfo() {
  const url = '/api/v0/chaininfo';
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
    .then(response => response.json());
}

function getBlockByHash(id) {
  const url = '/api/v0/block';
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
    .then(response => response.json());
}

function getBlockByHeight(id) {
  const url = '/api/v0/blockheight';
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

function getBlockStats(id) {
  const url = '/api/v0/blockstats';
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
    .then(response => response.json());
}

function getTransaction(id) {
  const url = '/api/v0/tx';
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
    .then(response => response.json());
}

function getAddress(address, startHeight, endHeight) {
  const url = '/api/v0/address';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      start_height: startHeight,
      end_height: endHeight,
      addresses: [address],
      chain: 'testnet3',
    }),
  };
  return fetch(url, requestParams)
    .then(response => response.json());
}

module.exports = {
  getChainInfo,
  getBlockByHash,
  getBlockByHeight,
  getBlockStats,
  getTransaction,
  getAddress,
};
