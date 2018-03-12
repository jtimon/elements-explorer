import React, { Component } from 'react';
import { render } from 'react-dom';
import { Link } from 'react-router-dom';

import api from '../api.js';
import format from '../utils/format.js';
import utils from '../utils/utils.js';

import Jumbotron from './jumbotron.jsx';
import TransactionJumbotron from './jumbotron_transaction.jsx';
import Transaction from './transaction.jsx';

class TransactionPage extends Component {
    constructor(props) {
      super(props);
      this.loadTx = this.loadTx.bind(this);
      this.state = {
        block: {},
        transaction: {}
      };
    }

    componentDidMount() {
        this.loadTx(this.props.match.params.txid);
    }

    componentWillReceiveProps(nextProps) {
        this.loadTx(nextProps.match.params.txid);
    }

    loadTx(txid) {
      function processTx(tx) {
        let promise = Promise.resolve();
        for (let i = 0; i < tx.vin.length; i++) {
            if (tx.vin[i].txid) {
              let vout = tx.vin[i].vout;
               promise = promise.then(() => {
                  return api.apiGetTransaction(tx.vin[i].txid).then((vin) => {
                      tx.vin[i].tx = vin.vout[vout];
                  })
               })
            }
        }
        promise = promise.then(() => {
          loadedTransaction = tx;
        });
        return promise;
      }
      let loadedTransaction = {};
      let loadedBlock = {};
      api.apiGetTransaction(txid).then(processTx)
      .then(() => {
          let promise = Promise.resolve();
          promise = promise.then(() => {
            return api.apiGetBlockByHash(loadedTransaction.blockhash).then((block) => {
              loadedBlock = block;
            });
          });
          return promise;
      })
      .then(() => {
          this.setState({
            transaction: loadedTransaction,
            block: loadedBlock
          });
      });
    }

    render() {
      let tx = this.state.transaction;
      let block = this.state.block;
      let time = block.mediantime;
      let formattedTime = time ? format.formatDate(time * 1000) : '';
      window.state = this.state;
      let txLoaded = !utils.isEmpty(tx);
      return (
        <div>
          <Jumbotron component={(props) => (
              <TransactionJumbotron tx={tx} />
          )} pageType={'transaction-page'} />
          <div className="container">
            <div className="block-stats-table">
              <div>
                <div>Timestamp</div>
                <div></div>
              </div>
              <div>
                <div>Size (KB)</div>
                <div>{tx.size}</div>
              </div>
              <div>
                <div>Weight (KWU)</div>
                <div></div>
              </div>
              <div>
                <div>Included in Block</div>
                <div><Link to={'/gui2/block/' + tx.blockhash}>{tx.blockhash}</Link></div>
              </div>
              <div>
                <div>Value</div>
                <div></div>
              </div>
            </div>
            {(txLoaded) ? (
              <Transaction tx={tx} time={formattedTime} block={block} />
            ): null}
          </div>
        </div>
      );
    }
}

export default TransactionPage;
