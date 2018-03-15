const redux = require('redux');
const Immutable = require('seamless-immutable').static;

function createStore() {
  function reducer(state, action) {
    switch (action.type) {
      case 'MERGE':
        return Immutable.merge(state, action.data);
      default:
        return state;
    }
  }

  const store = redux.createStore(reducer, Immutable.from({}));

  function dispatchMerge(data) {
    store.dispatch({
      data,
      type: 'MERGE',
    });
  }

  store.dispatchMerge = dispatchMerge;
  return store;
}

export default createStore;
