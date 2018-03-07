import React, { Component } from 'react';
import { render } from 'react-dom';
import { Link } from 'react-router-dom';

import api from '../api.js';
import format from '../utils/format.js';

import Jumbotron from './jumbotron.jsx';
import BlockJumbotron from './jumbotron_block.jsx';

class Transaction extends Component {
    render() {
        function generateVIn(tx) {
          if (tx.vin) {
            return tx.vin.map((vin) => {
              if (vin.tx) {
                return vin.tx.scriptPubKey.addresses.map((addr, i) => {
                  return (
                    <div key={i}>
                      <a href="#">{addr}</a>
                    </div>
                  );
                });
              } else if (vin.coinbase) {
                return (<div key="coinbase">Coinbase</div>);
              }
            });
          }
          return null;
        }

        function generateVOut(tx) {
          return tx.vout.map((vout) => {
            return vout.scriptPubKey.addresses.map((addr, i) => {
              return (
                <div key={i}>
                  <a href="#">{addr}</a>
                </div>
              );
            });
          })
        }

        let tx = this.props.tx;
        return (
          <div className="transaction-box">
            <div className="header">
              <div>
                <a href="#">{tx.txid}</a>
              </div>
              <div>
                <div>
                  <div>Advanced Details</div>
                  <div>
                    <img src="/gui2/static/img/icons/plus.svg" />
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
                <span>Confirmations</span>
                <span></span>
              </div>
            </div>
          </div>
        )
    }
}

export default Transaction;
