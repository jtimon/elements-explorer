import React, { Component } from 'react';
import { render } from 'react-dom';

class TransactionJumbotron extends Component {
    render() {
        let tx = this.props.tx;
        return (
            <div className="container">
              <h1>Transaction</h1>
              <p className="block-hash">{tx.txid} <img src="/gui2/static/img/icons/code.svg" /></p>
            </div>
        );
    }
}

export default TransactionJumbotron;
