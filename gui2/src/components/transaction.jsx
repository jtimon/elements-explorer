import React, { Component } from 'react';
import { render } from 'react-dom';
import { Link } from 'react-router-dom';

import api from '../api.js';
import dom from '../utils/dom.js';
import format from '../utils/format.js';

import Jumbotron from './jumbotron.jsx';
import BlockJumbotron from './jumbotron_block.jsx';

class Transaction extends Component {
    constructor(props) {
      super(props);
      this.toggleAdvanced = this.toggleAdvanced.bind(this);
      this.state = {
        show_advanced: false
      };
    }

    toggleAdvanced() {
      this.setState({
        show_advanced: !this.state.show_advanced
      });
    }

    render() {
        function generateVIn(tx) {
          if (tx.vin) {
            return tx.vin.map((vin) => {
              if (vin.tx) {
                return vin.tx.scriptPubKey.addresses.map((addr, i) => {
                  return (
                    <div key={i} className={dom.classNames('vin', dom.classIf(showAdvanced, 'active'))}>
                      <div className="vin-header">
                        <a href="#">{addr}</a>
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
                  );
                });
              } else if (vin.coinbase) {
                return (
                  <div key="coinbase" className="vin">
                    <div className="vin-header">Coinbase</div>
                  </div>
                );
              }
            });
          }
          return null;
        }

        function generateVOut(tx) {
          return tx.vout.map((vout, i) => {
            let scriptPubKey = vout.scriptPubKey;
            return (
              <div key={i} className={dom.classNames('vout', dom.classIf(showAdvanced, 'active'))}>
                <div className="vout-header">
                  <a href="#">{(scriptPubKey.addresses) ? scriptPubKey.addresses[0] : 'nonstandard'}</a>
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
                <a href="#">{tx.txid}</a>
              </div>
              <div>
                <div onClick={this.toggleAdvanced}>
                  <div>Advanced Details</div>
                  <div>
                    {(showAdvanced) ? (
                      <img src="/gui2/static/img/icons/minus.svg" />
                    ) : (
                      <img src="/gui2/static/img/icons/plus.svg" />
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
                  <span className="helper"></span>
                  <img src="/gui2/static/img/icons/peg-in.svg" />
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
              <div></div>
              <div>
                <span>{this.props.block.confirmations} Confirmations</span>
                <span></span>
              </div>
            </div>
          </div>
        )
    }
}

export default Transaction;
