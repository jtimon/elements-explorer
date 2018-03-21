
function isEmpty(obj) {
  return Object.keys(obj).length === 0 && obj.constructor === Object;
}

function addBlockToStore(obj, data) {
  const blockHash = data.hash;
  const blockHeight = data.height;
  let newObj = obj;
  newObj = Immutable.setIn(newObj, ['hashes', blockHash], data);
  newObj = Immutable.setIn(newObj, ['heights', blockHeight], blockHash);
  return newObj;
}

module.exports = {
  addBlockToStore,
  isEmpty,
};
