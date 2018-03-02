
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

module.exports = {
    formatNumber
}
