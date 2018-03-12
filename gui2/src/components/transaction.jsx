import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

import dom from '../utils/dom';

class Transaction extends Component {
  constructor(props) {
    super(props);
    this.toggleAdvanced = this.toggleAdvanced.bind(this);
    this.state = {
      show_advanced: false,
    };
  }

  toggleAdvanced() {
    this.setState({
      show_advanced: !this.state.show_advanced,
    });
  }

  render() {
    function generateVIn(tx) {
      if (tx.vin) {
        return tx.vin.map((vin) => {
          if (vin.tx) {
            return vin.tx.scriptPubKey.addresses.map(addr => (
              <div key={vin.tx.n} className={dom.classNames('vin', dom.classIf(showAdvanced, 'active'))}>
                <div className="vin-header">
                  <a href="#addr">{addr}</a>
                </div>
                <div className={dom.classNames('vin-body', dom.showIf(showAdvanced))}>
                  <div>
                    <div>scriptSig.ASM</div>
                    <div>{vin.scriptSig.asm}</div>
                  </div>
                  <div>
                    <div>scriptSig.hex</div>
                    <div>{vin.scriptSig.hex}</div>
                  </div>
                </div>
              </div>
            ));
          } else if (vin.coinbase) {
            return (
              <div key="coinbase" className="vin">
                <div className="vin-header">Coinbase</div>
              </div>
            );
          }
          return null;
        });
      }
      return null;
    }

    function generateVOut(tx) {
      return tx.vout.map((vout, i) => {
        const scriptPubKey = vout.scriptPubKey;
        return (
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

    let tx = this.props.tx;
    let showAdvanced = this.state.show_advanced;
    return (
      <div className="transaction-box">
        <div className="header">
          <div>
            <Link to={`/gui2/tx/${tx.txid}`}>{tx.txid}</Link>
          </div>
          <div>
            <div role="button" tabIndex={0} onClick={this.toggleAdvanced} onKeyPress={this.toggleAdvanced}>
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
            {generateVIn(tx)}
          </div>
          <div>
            <div>
              <span className="helper" />
              <img alt="" src="/gui2/static/img/icons/peg-in.svg" />
            </div>
          </div>
          <div className="vouts">
            {generateVOut(tx)}
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
  tx: PropTypes.object.isRequired,
  block: PropTypes.object.isRequired,
  time: PropTypes.string.isRequired,
};

export default Transaction;
