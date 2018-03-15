import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';

import api from './utils/api';
import createStore from './store';

import App from './components/app';

const Immutable = require('seamless-immutable').static;

const store = createStore();

window.store = store;

function Body() {
  return (
    <Provider store={store}>
      <App />
    </Provider>
  );
}

function initStateValues() {
  store.dispatchMerge({
    chain_info: Immutable({}),
    blocks: Immutable({}),
    transactions: Immutable({}),
  });
}

function loadChainInfo() {
  // make async call to api, handle promise, dispatch action when promise is resolved
  return api.getChainInfo()
    .then((data) => {
      store.dispatchMerge({
        chain_info: data,
      });
    })
    .catch((error) => {
      throw (error);
    });
}

initStateValues();
loadChainInfo().then(() => ( // FIXME: Don't wait for chain info load to render
  render(<Body />, document.getElementById('liquid-explorer'))
));
