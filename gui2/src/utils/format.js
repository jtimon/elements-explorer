import moment from 'moment-timezone';

function formatNumber(num) {
    let numString = num.toString();
    let formattedNumber = [];
    for (let i = 0, n = numString.length; i < n; i++) {
        if (i > 0 && i % 3 === 0) {
            formattedNumber.unshift(',');
        }
        formattedNumber.unshift(numString[n - i - 1]);
    }
    return formattedNumber.join('');
}

function formatDate(date, format = "ddd, D MMM YYYY HH:mm:ss zz") {
    return moment(date).tz(moment.tz.guess()).format(format).toString();
}

module.exports = {
    formatDate,
    formatNumber
}
