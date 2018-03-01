function api_chaininfo() {
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
  })
}

function api_getblock(id) {
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
  })
}

module.exports = {
  api_chaininfo,
  api_getblock,
}
