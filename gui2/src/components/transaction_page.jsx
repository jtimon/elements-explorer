import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

import api from '../utils/api';
import format from '../utils/format';
import utils from '../utils/utils';

import Jumbotron from './jumbotron';
import TransactionJumbotron from './jumbotron_transaction';
import Transaction from './transaction';

class TransactionPage extends Component {
  constructor(props) {
    super(props);
    this.loadTx = this.loadTx.bind(this);
    this.state = {
      block: {},
      transaction: {},
    };
  }

  componentDidMount() {
    this.loadTx(this.props.match.params.txid);
  }

  componentWillReceiveProps(nextProps) {
    this.loadTx(nextProps.match.params.txid);
  }

  loadTx(txid) {
    let loadedTransaction = {};
    let loadedBlock = {};

    api.getTransaction(txid)
      .then((tx) => {
        loadedTransaction = tx;

        let promise = Promise.resolve();
        promise = promise.then(() => api.getBlockByHash(loadedTransaction.blockhash)
          .then((block) => {
            loadedBlock = block;
          }));
        return promise;
      })
      .then(() => {
        this.setState({
          transaction: loadedTransaction,
          block: loadedBlock,
        });
      });
  }

  render() {
    const tx = this.state.transaction;
    const { block } = this.state;
    const time = block.mediantime;
    const formattedTime = time ? format.formatDate(time * 1000) : '';
    const txLoaded = !utils.isEmpty(tx);
    return (
      <div>
        <Jumbotron
          component={() => (
            <TransactionJumbotron
              tx={tx}
            />
          )}
          pageType="transaction-page"
        />
        <div className="container">
          <div className="block-stats-table">
            <div>
              <div>Timestamp</div>
              <div />
            </div>
            <div>
              <div>Size (KB)</div>
              <div>{tx.size}</div>
            </div>
            <div>
              <div>Weight (KWU)</div>
              <div />
            </div>
            <div>
              <div>Included in Block</div>
              <div><Link to={`/gui2/block/${tx.blockhash}`}>{tx.blockhash}</Link></div>
            </div>
            <div>
              <div>Value</div>
              <div />
            </div>
          </div>
          {(txLoaded) ? (
            <Transaction transaction={tx} time={formattedTime} block={block} />
          ) : null}
        </div>
      </div>
    );
  }
}
TransactionPage.propTypes = {
  match: PropTypes.shape({
    isExact: PropTypes.bool,
    params: PropTypes.object.isRequired,
    path: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
  }).isRequired,
};


export default TransactionPage;
