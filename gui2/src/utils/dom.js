function classIf(condition, className) {
  return (condition) ? className : '';
}

function classNames(...args) {
  return args.join(' ');
}

function showIf(condition) {
  return (condition) ? '' : 'hide';
}

export default {
  classIf,
  classNames,
  showIf,
};
