import React, { Component } from 'react';
import { render } from 'react-dom';
import { Link } from 'react-router-dom';

import api from '../api.js';
import format from '../utils/format.js';

import Jumbotron from './jumbotron.jsx';
import BlockJumbotron from './jumbotron_block.jsx';
import Transaction from './transaction.jsx';

class BlockPage extends Component {
    constructor(props) {
      super(props);
      this.loadBlock = this.loadBlock.bind(this);
      this.state = {
        block: {},
        transactions: []
      };
    }

    componentDidMount() {
        this.loadBlock(this.props.match.params.blockhash);
    }

    componentWillReceiveProps(nextProps) {
        this.loadBlock(nextProps.match.params.blockhash);
    }

    loadBlock(blockhash) {
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
          loadedTransactions.push(tx);
          return promise;
        }
        let loadedBlock = {};
        let loadedTransactions = [];
        api.apiGetBlockByHash(blockhash)
        .then((block) => {
            loadedBlock = block;
            let promise = Promise.resolve();
            for (let i = 0; i < block.tx.length; i++) {
               promise = promise.then(() => {
                 return api.apiGetTransaction(block.tx[i]).then(processTx);
               });
            }
            return promise;
        })
        .finally(() => {
          this.setState({
            block: loadedBlock,
            transactions: loadedTransactions
          });
        });
    }

    render() {
        function generateTransactions() {
          return loadedTransactions.map((tx) => {
            return (<Transaction key={tx.txid} tx={tx} time={formattedTime} />);
          })
        }
        let loadedTransactions = this.state.transactions;
        let block = this.state.block;
        let time = block.mediantime;
        let formattedTime = time ? format.formatDate(time * 1000) : '';
        let transactionCount = (block.tx) ? block.tx.length : 0;
        return (
          <div>
            <Jumbotron component={(props) => (
                <BlockJumbotron block={block} />
            )} pageType={'block-page'} />
            <div className="container">
              <div className="block-stats-table">
                <div>
                  <div>Height</div>
                  <div><Link to={'/gui2/block/' + block.hash}>{block.height}</Link></div>
                </div>
                <div>
                  <div>Confirmations</div>
                  <div>{block.confirmations}</div>
                </div>
                <div>
                  <div>Timestamp</div>
                  <div>{formattedTime}</div>
                </div>
                <div>
                  <div>Size (KB)</div>
                  <div>{block.size}</div>
                </div>
                <div>
                  <div>Weight (KWU)</div>
                  <div>{block.weight}</div>
                </div>
                <div>
                  <div>Version</div>
                  <div>{block.version}</div>
                </div>
              </div>
              <div className="transactions">
                <h3>{transactionCount} Transactions</h3>
                {generateTransactions()}
              </div>
            </div>
          </div>
        );
    }
}

export default BlockPage;
