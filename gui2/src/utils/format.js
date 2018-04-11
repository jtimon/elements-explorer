import moment from 'moment-timezone';

function trim(str) {
  return str.replace(/^\s+|\s+$/g, '');
}

function formatNumber(num) {
  const numString = num.toString();
  const formattedNumber = [];
  [...numString].forEach((c, i) => {
    if (i > 0 && (i % 3 === 0)) {
      formattedNumber.unshift(',');
    }
    formattedNumber.unshift(numString[numString.length - i - 1]);
  });
  return formattedNumber.join('');
}

function formatDate(date, format = 'ddd, D MMM YYYY HH:mm:ss zz') {
  return moment(date).tz(moment.tz.guess()).format(format).toString();
}

function capitalizeFirstLetter(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

module.exports = {
  capitalizeFirstLetter,
  formatDate,
  formatNumber,
  trim,
};
