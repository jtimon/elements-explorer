import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

import api from '../utils/api';
import format from '../utils/format';

import Jumbotron from './jumbotron';
import BlockJumbotron from './jumbotron_block';
import Transaction from './transaction';

class BlockPage extends Component {
  constructor(props) {
    super(props);
    this.loadBlock = this.loadBlock.bind(this);
    this.state = {
      block: {},
      block_stats: {},
      transactions: [],
    };
  }

  componentDidMount() {
    this.loadBlock(this.props.match.params.blockhash);
  }

  componentWillReceiveProps(nextProps) {
    this.loadBlock(nextProps.match.params.blockhash);
  }

  loadBlock(blockhash) {
    const loadedTransactions = [];
    let loadedBlock = {};
    let blockStats = {};

    function processTx(tx) {
      let promise = Promise.resolve();
      tx.vin.forEach((vin) => {
        if (vin.txid) {
          const { vout } = vin;
          promise = promise.then(() => (
            api.getTransaction(vin.txid)
              .then((vinTx) => {
                // eslint-disable-next-line no-param-reassign
                vin.tx = vinTx.vout[vout];
              })
          ));
        }
      });
      loadedTransactions.push(tx);
      return promise;
    }

    api.getBlockByHash(blockhash)
      .then((block) => {
        loadedBlock = block;
        let promise = Promise.resolve();
        promise = promise.then(() => (
          api.getBlockStats(block.height)
            .then((stats) => {
              blockStats = stats;
            })
        ));
        block.tx.forEach((tx) => {
          promise = promise.then(() => (
            api.getTransaction(tx)
              .then(processTx)
          ));
        });
        return promise;
      })
      .finally(() => {
        this.setState({
          block: loadedBlock,
          block_stats: blockStats,
          transactions: loadedTransactions,
        });
      });
  }

  render() {
    window.state = this.state;
    const { block } = this.state;
    const loadedTransactions = this.state.transactions;
    const blockStats = this.state.block_stats;
    const time = block.mediantime;
    const formattedTime = time ? format.formatDate(time * 1000) : '';
    const transactionCount = (block.tx) ? block.tx.length : 0;

    function generateTransactions() {
      return loadedTransactions.map(tx => (
        <Transaction key={tx.txid} transaction={tx} time={formattedTime} block={block} />
      ));
    }

    return (
      <div>
        <Jumbotron
          component={() => (
            <BlockJumbotron
              block={block}
            />
          )}
          pageType="block-page"
        />
        <div className="container">
          <div className="block-stats-table">
            <div>
              <div>Height</div>
              <div><Link to={`/gui2/block/${block.hash}`}>{block.height}</Link></div>
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
          <div className="transaction-stats">
            <h3>Transaction Stats</h3>
            <p>{block.merkleroot}</p>
            <div className="transaction-stats-boxes d-flex justify-content-between">
              <div className="box-wrapper">
                <div className="transaction-stats-box">
                  <div className="box-header">
                    <span>Fee</span>
                  </div>
                  <div className="box-body">
                    <div>
                      <span>Min</span>
                      <span>{blockStats.minfee}</span>
                    </div>
                    <div>
                      <span>Max</span>
                      <span>{blockStats.maxfee}</span>
                    </div>
                    <div>
                      <span>Avg</span>
                      <span>{blockStats.avgfee}</span>
                    </div>
                    <div>
                      <span>Median</span>
                      <span>{blockStats.medianfee}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="box-wrapper">
                <div className="transaction-stats-box">
                  <div className="box-header">
                    <span>Fee Rate</span>
                  </div>
                  <div className="box-body">
                    <div>
                      <span>Min</span>
                      <span>{blockStats.minfeerate}</span>
                    </div>
                    <div>
                      <span>Max</span>
                      <span>{blockStats.maxfeerate}</span>
                    </div>
                    <div>
                      <span>Avg</span>
                      <span>{blockStats.avgfeerate}</span>
                    </div>
                    <div>
                      <span>Median</span>
                      <span>{blockStats.medianfeerate}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="box-wrapper">
                <div className="transaction-stats-box">
                  <div className="box-header">
                    <span>Transaction Size</span>
                  </div>
                  <div className="box-body">
                    <div>
                      <span>Min</span>
                      <span>{blockStats.mintxsize}</span>
                    </div>
                    <div>
                      <span>Max</span>
                      <span>{blockStats.maxtxsize}</span>
                    </div>
                    <div>
                      <span>Avg</span>
                      <span>{blockStats.avgtxsize}</span>
                    </div>
                    <div>
                      <span>Median</span>
                      <span>{blockStats.mediantxsize}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="block-stats-table">
              <div>
                <div>Inputs</div>
                <div>{blockStats.ins}</div>
              </div>
              <div>
                <div>Outputs</div>
                <div>{blockStats.outs}</div>
              </div>
              <div>
                <div>UTXO Increase</div>
                <div>{blockStats.utxo_increase}</div>
              </div>
              <div>
                <div>UTXO Size Increase</div>
                <div>{blockStats.utxo_size_inc}</div>
              </div>
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
BlockPage.propTypes = {
  match: PropTypes.shape({
    isExact: PropTypes.bool,
    params: PropTypes.object.isRequired,
    path: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
  }).isRequired,
};

export default BlockPage;
