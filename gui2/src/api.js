function apiChainInfo() {
  const url = 'http://localhost:5000/api/v0/chaininfo'
  let requestParams = {
      method: 'POST',
      headers: {
        'Content-type': 'application/json'
      },
      body: JSON.stringify({
        chain: 'testnet3',
        id: 'testnet3'
      })
  }
  return fetch(url, requestParams)
  .then((response) => {
    return response.json();
  }).then((data) => {
    return data;
  });
}

function apiGetBlockByHash(id) {
  const url = 'http://localhost:5000/api/v0/block'
  let requestParams = {
      method: 'POST',
      headers: {
        'Content-type': 'application/json'
      },
      body: JSON.stringify({
        chain: 'testnet3',
        id: id
      })
  }
  return fetch(url, requestParams)
  .then((response) => {
    return response.json();
  }).then((data) => {
    return data;
  });
}

function apiGetBlockByHeight(id) {
  const url = 'http://localhost:5000/api/v0/blockheight'
  let requestParams = {
      method: 'POST',
      headers: {
        'Content-type': 'application/json'
      },
      body: JSON.stringify({
        chain: 'testnet3',
        id: id
      })
  }
  return fetch(url, requestParams)
  .then((response) => {
    return response.json();
  }).then((data) => {
    return data;
  });
}

function apiGetBlockStats(id) {
  const url = 'http://localhost:5000/api/v0/blockstats'
  let requestParams = {
      method: 'POST',
      headers: {
        'Content-type': 'application/json'
      },
      body: JSON.stringify({
        chain: 'testnet3',
        id: id
      })
  }
  return fetch(url, requestParams)
  .then((response) => {
    return response.json();
  }).then((data) => {
    return data;
  });
}

function apiGetTransaction(id) {
  const url = 'http://localhost:5000/api/v0/tx'
  let requestParams = {
      method: 'POST',
      headers: {
        'Content-type': 'application/json'
      },
      body: JSON.stringify({
        chain: 'testnet3',
        id: id
      })
  }
  return fetch(url, requestParams)
  .then((response) => {
    return response.json();
  }).then((data) => {
    return data;
  });
}

module.exports = {
  apiChainInfo,
  apiGetBlockByHash,
  apiGetBlockByHeight,
  apiGetBlockStats,
  apiGetTransaction
}
