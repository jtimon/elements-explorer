import utils from './utils';

const has = Object.prototype.hasOwnProperty;

function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}

function getAvailableChains() {
  const state = store.getState();
  if (!utils.isEmpty(state.availableChains)) {
    return Promise.resolve().then(() => state.availableChains);
  }
  const url = '/api/v0/available_chains';
  const requestParams = {
    method: 'GET',
  };
  return fetch(url, requestParams)
    .then(handleErrors)
    .then(response => response.json())
    .then((data) => {
      store.dispatchMerge({
        availableChains: data.available_chains,
      });
      return data;
    });
}

function getChainInfo() {
  const state = store.getState();
  const { chain } = state;
  if (!utils.isEmpty(state.chainInfo)) {
    return Promise.resolve().then(() => state.chainInfo);
  }
  const url = '/api/v0/chaininfo';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      chain,
      id: chain,
    }),
  };
  return fetch(url, requestParams)
    .then(handleErrors)
    .then(response => response.json())
    .then((data) => {
      store.dispatchMerge({
        chainInfo: data,
      });
      return data;
    });
}

function getAllChainInformation() {
  return getAvailableChains().then(() => (
    getChainInfo()
  ));
}

function getBlockByHash(id) {
  const state = store.getState();
  const { chain } = state;
  if (!utils.isEmpty(state.blocks.hashes)) {
    if (has.call(state.blocks.hashes, id)) {
      return Promise.resolve().then(() => state.blocks.hashes[id]);
    }
  }
  const url = '/api/v0/block';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      chain,
      id,
    }),
  };
  return fetch(url, requestParams)
    .then(handleErrors)
    .then(response => response.json())
    .then((data) => {
      const { blocks } = store.getState();
      store.dispatchMerge({
        blocks: utils.addBlockToStore(blocks, data),
      });
      return data;
    });
}

function getBlockByHeight(id) {
  const state = store.getState();
  const { chain } = state;
  if (!utils.isEmpty(state.blocks.heights)) {
    if (has.call(state.blocks.heights, id)) {
      const blockHash = state.blocks.heights[id];
      return Promise.resolve().then(() => state.blocks.hashes[blockHash]);
    }
  }
  const url = '/api/v0/blockheight';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      chain,
      id,
    }),
  };
  return fetch(url, requestParams)
    .then(handleErrors)
    .then(response => response.json())
    .then((data) => {
      const { blocks } = store.getState();
      store.dispatchMerge({
        blocks: utils.addBlockToStore(blocks, data),
      });
      return data;
    });
}

function getBlockStats(id) {
  const state = store.getState();
  const { chain } = state;
  if (!utils.isEmpty(state.blocks.stats)) {
    if (has.call(state.blocks.stats, id)) {
      return Promise.resolve().then(() => state.blocks.stats[id]);
    }
  }
  const url = '/api/v0/blockstats';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      chain,
      id,
    }),
  };
  return fetch(url, requestParams)
    .then(handleErrors)
    .then(response => response.json())
    .then((data) => {
      const { blocks } = store.getState();
      store.dispatchMerge({
        blocks: Immutable.setIn(blocks, ['stats', id], data),
      });
      return data;
    });
}

function getTransaction(id, chainParam) {
  const state = store.getState();
  let chain = chainParam;
  if (!chain) {
    ({ chain } = state);
  }
  if (!utils.isEmpty(state.transactions)) {
    if (has.call(state.transactions[chain], id)) {
      return Promise.resolve().then(() => state.transactions[chain][id]);
    }
  }
  const url = '/api/v0/tx';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      chain,
      id,
    }),
  };
  return fetch(url, requestParams)
    .then(handleErrors)
    .then(response => response.json())
    .then((data) => {
      const { transactions } = store.getState();
      store.dispatchMerge({
        transactions: Immutable.setIn(transactions, [chain, id], data),
      });
      return data;
    });
}

function getAddress(address, startHeight, endHeight) {
  const state = store.getState();
  const { chain } = state;
  const url = '/api/v0/address';
  const requestParams = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      chain,
      start_height: startHeight,
      end_height: endHeight,
      addresses: [address],
    }),
  };
  return fetch(url, requestParams)
    .then(handleErrors)
    .then(response => response.json());
}

module.exports = {
  getAvailableChains,
  getAllChainInformation,
  getChainInfo,
  getBlockByHash,
  getBlockByHeight,
  getBlockStats,
  getTransaction,
  getAddress,
};
