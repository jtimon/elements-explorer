import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

import api from '../utils/api';
import dom from '../utils/dom';
import utils from '../utils/utils';

import VIn from './transaction_vin';
import VOut from './transaction_vout';

class Transaction extends Component {
  static isPegOutTx(tx) {
    for (let i = 0; i < tx.vout.length; i += 1) {
      if ('pegout_type' in tx.vout[i].scriptPubKey) {
        return true;
      }
    }
    return false;
  }

  static isConfidentialTx(tx) {
    for (let i = 0; i < tx.vout.length; i += 1) {
      if ('ct-bits' in tx.vout[i]) {
        return true;
      }
    }
    return false;
  }

  static totalVOutValue(tx) {
    let sum = 0;
    for (let i = 0; i < tx.vout.length; i += 1) {
      if (!('ct-bits' in tx.vout[i])) {
        sum += tx.vout[i].value;
      }
    }
    return sum;
  }

  constructor(props) {
    super(props);
    this.loadVIns = this.loadVIns.bind(this);
    this.toggleAdvanced = this.toggleAdvanced.bind(this);
    this.state = {
      showAdvanced: false,
      vins: [],
      is_pegin: false,
    };
  }

  componentDidMount() {
    this.loadVIns(this.props.transaction);
  }

  loadVIns(tx) {
    const vins = [];
    const promises = [];
    let isPegIn = false;
    tx.vin.forEach((vin, i) => {
      if (vin.is_pegin) {
        const { availableChains, chain } = this.props;
        const parentChain = availableChains[chain].parent_chain;
        isPegIn = true;
        if (parentChain) {
          promises.push(Promise.resolve().then(() => (
            api.getTransaction(vin.txid, parentChain).then((data) => {
              const [address] = data.vout[vin.vout].scriptPubKey.addresses;
              vins[i] = {
                address,
                coinbase: false,
                pegin: true,
                txid: vin.txid,
                vout: vin.vout,
              };
              return data;
            })
          )));
        } else {
          vins[i] = {
            coinbase: false,
            pegin: true,
            txid: vin.txid,
            vout: vin.vout,
          };
        }
      } else if (vin.txid) {
        promises.push(Promise.resolve().then(() => (
          api.getTransaction(vin.txid).then((data) => {
            vins[i] = {
              coinbase: false,
              pegin: false,
              txid: vin.txid,
              vout: vin.vout,
            };
            return data;
          })
        )));
      } else {
        vins[i] = {
          coinbase: true,
          pegin: false,
          txid: undefined,
          vout: undefined,
        };
      }
    });
    Promise.all(promises).then(() => {
      this.setState({
        vins,
        is_pegin: isPegIn,
      });
    });
  }

  toggleAdvanced() {
    this.setState({
      showAdvanced: !this.state.showAdvanced,
    });
  }

  render() {
    const { chainInfo, transaction } = this.props;
    const { showAdvanced, vins } = this.state;
    const confirmations = (chainInfo.blocks - this.props.block.height) + 1;
    const confirmationsString = (confirmations === 1) ? 'Confirmation' : 'Confirmations';
    const isPegIn = this.state.is_pegin;
    const isPegOut = Transaction.isPegOutTx(transaction);
    const isConfidential = Transaction.isConfidentialTx(transaction);
    const totalValue = Transaction.totalVOutValue(transaction);

    function generateVIn() {
      if (utils.isEmptyArray(vins)) {
        return (
          <div className="vin-loading">
            <img alt="" src="/static/img/Loading.gif" />
          </div>
        );
      }
      return vins.map((vin, i) => (
        // eslint-disable-next-line react/no-array-index-key
        <VIn key={i} index={i} transaction={transaction} vin={vin} showAdvanced={showAdvanced} />
      ));
    }

    function generateVOut(tx) {
      return tx.vout.map((vout, i) => (
        // eslint-disable-next-line react/no-array-index-key
        <VOut key={i} vout={vout} showAdvanced={showAdvanced} />
      ));
    }

    return (
      <div className="transaction-box">
        <div className="header">
          <div>
            <Link to={`/tx/${transaction.txid}`}>{transaction.txid}</Link>
          </div>
          <div>
            <div
              role="button"
              tabIndex={0}
              onClick={this.toggleAdvanced}
              onKeyPress={this.toggleAdvanced}
            >
              <div>Advanced Details</div>
              <div>
                {(showAdvanced) ? (
                  <img alt="" src="/static/img/icons/minus.svg" />
                ) : (
                  <img alt="" src="/static/img/icons/plus.svg" />
                )}
              </div>
            </div>
          </div>
        </div>
        <div className="ins-and-outs">
          <div className="vins">
            {generateVIn()}
          </div>
          <div>
            <div>
              <span className="helper" />
              <img className={dom.showIf(isPegOut)} alt="" src="/static/img/icons/peg-out.svg" />
              <img className={dom.showIf(isPegIn)} alt="" src="/static/img/icons/peg-in.svg" />
              <img className={dom.showIf(!isPegIn && !isPegOut)} alt="" src="/static/img/icons/arrow-r.svg" />
            </div>
          </div>
          <div className="vouts">
            {generateVOut(transaction)}
          </div>
        </div>
        <div className="footer">
          <div>
            <span>Transaction Time</span>
            <span>{this.props.time}</span>
          </div>
          <div />
          <div>
            <span>{confirmations} {confirmationsString}</span>
            <span>{(isConfidential) ? 'Confidential' : `${totalValue} BTC`}</span>
          </div>
        </div>
      </div>
    );
  }
}
Transaction.propTypes = {
  transaction: PropTypes.shape({}).isRequired,
  block: PropTypes.shape({
    confirmations: PropTypes.number,
    height: PropTypes.number.isRequired,
  }).isRequired,
  time: PropTypes.string.isRequired,
  availableChains: PropTypes.shape({}).isRequired,
  chain: PropTypes.string.isRequired,
  chainInfo: PropTypes.shape({}).isRequired,
};

const mapStateToProps = state => ({
  availableChains: state.availableChains,
  chain: state.chain,
  chainInfo: state.chainInfo,
});

export default connect(mapStateToProps)(Transaction);
