import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

import api from '../utils/api';
import dom from '../utils/dom';

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
      show_advanced: false,
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
        isPegIn = true;
        vins[i] = {
          coinbase: false,
          pegin: true,
          txid: undefined,
          vout: undefined,
        };
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
      show_advanced: !this.state.show_advanced,
    });
  }

  render() {
    const chainInfo = this.props.chain_info;
    const { transaction } = this.props;
    const { vins } = this.state;
    const showAdvanced = this.state.show_advanced;
    const confirmations = chainInfo.blocks - this.props.block.height;
    const isPegIn = this.state.is_pegin;
    const isPegOut = Transaction.isPegOutTx(transaction);
    const isConfidential = Transaction.isConfidentialTx(transaction);
    const totalValue = Transaction.totalVOutValue(transaction);

    function generateVIn() {
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
            <Link to={`/gui2/tx/${transaction.txid}`}>{transaction.txid}</Link>
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
                  <img alt="" src="/gui2/static/img/icons/minus.svg" />
                ) : (
                  <img alt="" src="/gui2/static/img/icons/plus.svg" />
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
              <img className={dom.showIf(isPegOut)} alt="" src="/gui2/static/img/icons/peg-out.svg" />
              <img className={dom.showIf(isPegIn)} alt="" src="/gui2/static/img/icons/peg-in.svg" />
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
            <span>{confirmations} Confirmations</span>
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
    confirmations: PropTypes.number.isRequired,
    height: PropTypes.number.isRequired,
  }).isRequired,
  time: PropTypes.string.isRequired,
  chain_info: PropTypes.shape({}).isRequired,
};

const mapStateToProps = state => ({
  chain_info: state.chain_info,
});

export default connect(mapStateToProps)(Transaction);
