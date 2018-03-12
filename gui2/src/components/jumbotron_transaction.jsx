import React from 'react';
import PropTypes from 'prop-types';

function TransactionJumbotron({ tx }) {
  return (
    <div className="container">
      <h1>Transaction</h1>
      <p className="block-hash">{tx.txid} <img alt="" src="/gui2/static/img/icons/code.svg" /></p>
    </div>
  );
}
TransactionJumbotron.propTypes = {
  tx: PropTypes.object.isRequired,
};


export default TransactionJumbotron;
