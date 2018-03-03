import React, { Component } from 'react';
import { render } from 'react-dom';
import { Link } from 'react-router-dom';

import utils from '../utils.js';

import Jumbotron from './jumbotron.jsx';
import BlockJumbotron from './jumbotron_block.jsx';

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
          loadedTransactions.push(tx);
        }
        let loadedBlock = {};
        let loadedTransactions = [];
        utils.apiGetBlockByHash(blockhash)
        .then((block) => {
            loadedBlock = block;
            let promise = Promise.resolve();
            for (let i = 0; i < block.tx.length; i++) {
               promise = promise.then(() => {
                 return utils.apiGetTransaction(block.tx[i]).then(processTx);
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
              return (
                <div key={tx.txid}>
                  <p>{tx.txid}</p>
                </div>
              )
           })
        }
        let loadedTransactions = this.state.transactions;
        let block = this.state.block;
        let time = new Date(block.mediantime * 1000);
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
                  <div>{time.toString()}</div>
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
              <div className="transactions-stats">
                <h3>{transactionCount} Transactions</h3>
                {generateTransactions()}
              </div>
            </div>
          </div>
        );
    }
}

export default BlockPage;
