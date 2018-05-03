function isEmptyArray(arr) {
  return arr === undefined || arr.length === 0;
}

function isEmptyObject(obj) {
  return Object.keys(obj).length === 0 && obj.constructor === Object;
}

function addBlockToStore(obj, data) {
  const blockHash = data.id;
  const blockHeight = data.height;
  let newObj = obj;
  newObj = Immutable.setIn(newObj, ['hashes', blockHash], data);
  newObj = Immutable.setIn(newObj, ['heights', blockHeight], blockHash);
  return newObj;
}

function isNaturalNumber(s) {
  return /^(0|([1-9]\d*))$/.test(s);
}

function isValidHash(s) {
  return /^[0-9a-f]{64}$/.test(s);
}

module.exports = {
  addBlockToStore,
  isEmptyArray,
  isEmptyObject,
  isNaturalNumber,
  isValidHash,
};
