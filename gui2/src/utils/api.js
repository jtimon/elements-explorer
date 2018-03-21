import utils from './utils';

const has = Object.prototype.hasOwnProperty;

function getChainInfo() {
  const state = store.getState();
  if (!utils.isEmpty(state.chain_info)) {
    return Promise.resolve().then(() => state.chain_info);
  }
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
    .then(response => response.json())
    .then((data) => {
      store.dispatchMerge({
        chain_info: data,
      });
      return data;
    });
}

function getBlockByHash(id) {
  const state = store.getState();
  if (!utils.isEmpty(state.blocks.hashes)) {
    if (has.call(state.blocks.hashes, id)) {
      return Promise.resolve().then(() => state.blocks.heights[id]);
    }
  }
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
    .then(response => response.json())
    .then((data) => {
      const { blocks } = state;
      store.dispatchMerge({
        blocks: utils.addBlockToStore(blocks, data),
      });
      return data;
    });
}

function getBlockByHeight(id) {
  const state = store.getState();
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
      id,
      chain: 'testnet3',
    }),
  };
  return fetch(url, requestParams)
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
      id,
      chain: 'testnet3',
    }),
  };
  return fetch(url, requestParams)
    .then(response => response.json())
    .then((data) => {
      const { blocks } = store.getState();
      store.dispatchMerge({
        blocks: Immutable.setIn(blocks, ['stats', id], data),
      });
      return data;
    });
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
