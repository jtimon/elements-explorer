import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import api from '../utils/api';
import dom from '../utils/dom';
import format from '../utils/format';

import Jumbotron from './jumbotron';
import BlockJumbotron from './jumbotron_block';
import Transaction from './transaction';
import NotFoundPage from './not_found_page';

class BlockPage extends Component {
  constructor(props) {
    super(props);
    this.loadBlock = this.loadBlock.bind(this);
    this.state = {
      block: {},
      blockStats: {},
      transactions: [],
      notFound: false,
    };
  }

  componentDidMount() {
    this.loadBlock(this.props.match.params.blockhash);
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.match.params.blockhash !== this.props.match.params.blockhash) {
      this.loadBlock(nextProps.match.params.blockhash);
    }
  }

  loadBlock(blockhash) {
    const { chain } = this.props;
    const transactions = [];

    api.getAllChainInformation()
      .then(() => {
        api.getBlockByHash(blockhash)
          .then((block) => {
            this.setState({
              block,
            });
            let promise = Promise.resolve();
            if (!['liquid'].includes(chain)) {
              promise = promise.then(() => (
                api.getBlockStats(block.height)
                  .then((blockStats) => {
                    this.setState({
                      blockStats,
                    });
                    return blockStats;
                  })
              ));
            }
            block.tx.forEach((tx) => {
              promise = promise.then(() => (
                api.getTransaction(tx)
                  .then((txData) => {
                    let hasTx = false;
                    for (let i = 0; i < transactions.length; i += 1) {
                      if (transactions[i] === txData) {
                        hasTx = true;
                      }
                    }
                    if (!hasTx) {
                      transactions.push(txData);
                    }
                    this.setState({
                      transactions,
                    });
                    return txData;
                  })
              ));
            });
            return promise;
          })
          .catch((err) => {
            const { error } = err;
            if (error && error.message === 'Block not found') {
              this.setState({
                notFound: true,
              });
            }
          });
      });
  }

  render() {
    const { block, blockStats, notFound } = this.state;

    if (notFound) {
      return (
        <NotFoundPage />
      );
    }

    const loadedTransactions = this.state.transactions;
    const { chain, chainInfo } = this.props;
    const hasBlockStats = !['liquid'].includes(chain);
    const time = block.mediantime;
    const formattedTime = time ? format.formatDate(time * 1000) : '';
    const transactionCount = (block.tx) ? block.tx.length : 0;
    const confirmations = (chainInfo.blocks - block.height) + 1;
    const blockSize = (block.size) ? block.size / 1000 : '';
    const blockWeight = (block.weight) ? block.weight / 1000 : '';

    const isLoading = !block.tx || (block.tx.length !== loadedTransactions.length);

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
              <div><Link to={`/block/${block.id}`}>{block.height}</Link></div>
            </div>
            <div>
              <div>Confirmations</div>
              <div>{Number.isNaN(confirmations) ? '' : confirmations}</div>
            </div>
            <div>
              <div>Timestamp</div>
              <div>{formattedTime}</div>
            </div>
            <div>
              <div>Size (KB)</div>
              <div>{blockSize}</div>
            </div>
            <div>
              <div>Weight (KWU)</div>
              <div>{blockWeight}</div>
            </div>
          </div>
          {(hasBlockStats) ? (
            <div className="transaction-stats">
              <h3>Transaction Stats</h3>
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
          ) : null}
          <div className="transactions">
            <h3>{transactionCount} Transactions</h3>
            <img className={dom.showIf(isLoading)} alt="" src="/static/img/Loading.gif" />
            {generateTransactions()}
            <div className={dom.classNames('transaction-box', 'loading-transaction', dom.showIf(isLoading))}>
              <img alt="" src="/static/img/Loading.gif" />
            </div>
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
  chain: PropTypes.string.isRequired,
  chainInfo: PropTypes.shape({}).isRequired,
};

const mapStateToProps = state => ({
  chain: state.chain,
  chainInfo: state.chainInfo,
});

export default connect(mapStateToProps)(BlockPage);
