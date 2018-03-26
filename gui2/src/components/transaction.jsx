import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

import api from '../utils/api';
import dom from '../utils/dom';

class Transaction extends Component {
  constructor(props) {
    super(props);
    this.loadVIns = this.loadVIns.bind(this);
    this.toggleAdvanced = this.toggleAdvanced.bind(this);
    this.state = {
      show_advanced: false,
      vins: [],
    };
  }

  componentDidMount() {
    this.loadVIns(this.props.transaction);
  }

  loadVIns(tx) {
    const vins = [];
    const promises = [];
    tx.vin.forEach((vin, i) => {
      if (vin.txid) {
        promises.push(Promise.resolve().then(() => (
          api.getTransaction(vin.txid).then((data) => {
            vins[i] = {
              coinbase: false,
              txid: vin.txid,
              vout: vin.vout,
            };
            return data;
          })
        )));
      } else {
        vins[i] = {
          coinbase: true,
          txid: undefined,
          vout: undefined,
        };
      }
    });
    Promise.all(promises).then(() => {
      this.setState({
        vins,
      });
    });
  }

  toggleAdvanced() {
    this.setState({
      show_advanced: !this.state.show_advanced,
    });
  }

  render() {
    const { transaction } = this.props;
    const { vins } = this.state;
    const storeTxs = store.getState().transactions;
    const showAdvanced = this.state.show_advanced;

    function generateVIn() {
      return vins.map((vin, i) => {
        if (vin.coinbase) {
          return (
            <div key="coinbase" className="vin">
              <div className="vin-header">Coinbase</div>
            </div>
          );
        } else if (vin.txid) {
          const tx = storeTxs[vin.txid].vout[vin.vout];
          const { scriptSig } = transaction.vin[i];
          return tx.scriptPubKey.addresses.map(addr => (
            <div key={tx.n} className={dom.classNames('vin', dom.classIf(showAdvanced, 'active'))}>
              <div className="vin-header">
                <a href="#addr">{addr}</a>
              </div>
              <div className={dom.classNames('vin-body', dom.showIf(showAdvanced))}>
                <div>
                  <div>scriptSig.ASM</div>
                  <div>{scriptSig.asm}</div>
                </div>
                <div>
                  <div>scriptSig.hex</div>
                  <div>{scriptSig.hex}</div>
                </div>
              </div>
            </div>
          ));
        }
        return null;
      });
    }

    function generateVOut(tx) {
      return tx.vout.map((vout, i) => {
        const { scriptPubKey } = vout;
        return (
          // eslint-disable-next-line react/no-array-index-key
          <div key={i} className={dom.classNames('vout', dom.classIf(showAdvanced, 'active'))}>
            <div className="vout-header">
              <a href="#addr">{(scriptPubKey.addresses) ? scriptPubKey.addresses[0] : 'nonstandard'}</a>
            </div>
            <div className={dom.classNames('vout-body', dom.showIf(showAdvanced))}>
              <div>
                <div>Type</div>
                <div>{scriptPubKey.type}</div>
              </div>
              <div>
                <div>scriptPubKey.hex</div>
                <div>{scriptPubKey.hex}</div>
              </div>
            </div>
          </div>
        );
      });
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
              <img alt="" src="/gui2/static/img/icons/peg-in.svg" />
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
            <span>{this.props.block.confirmations} Confirmations</span>
            <span />
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
  }).isRequired,
  time: PropTypes.string.isRequired,
};

export default Transaction;
