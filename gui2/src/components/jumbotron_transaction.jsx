import React, { Component } from 'react';
import PropTypes from 'prop-types';

import dom from '../utils/dom';
import utils from '../utils/utils';

import JumbotronTooltip from './jumbotron_tooltip';

class TransactionJumbotron extends Component {
  constructor(props) {
    super(props);
    this.handleMouseClick = this.handleMouseClick.bind(this);
    this.handleMouseClickClose = this.handleMouseClickClose.bind(this);
    this.state = {
      showCodeTooltip: false,
    };
  }

  handleMouseClick() {
    this.setState({
      showCodeTooltip: !this.state.showCodeTooltip,
    });
  }

  handleMouseClickClose() {
    this.setState({
      showCodeTooltip: false,
    });
  }

  render() {
    const { tx } = this.props;
    const tooltipData = tx.hex;
    const { showCodeTooltip } = this.state;
    const isLoading = utils.isEmpty(tx);

    return (
      <div className="container">
        <div className={dom.classNames('jumbotron-loading', dom.showIf(isLoading))}>
          <img alt="" src="/static/img/Loading.gif" />
        </div>
        <div className={dom.showIf(!isLoading)}>
          <h1>Transaction</h1>
          <div className="block-hash">
            <span>{(tx.txid) ? tx.txid : ''}</span>
            <JumbotronTooltip
              className={dom.showIf(tx.txid)}
              showCodeTooltip={showCodeTooltip}
              clickHandler={this.handleMouseClick}
              clickCloseHandler={this.handleMouseClickClose}
              header={`Transaction ${tx.txid}`}
              data={tooltipData}
            />
          </div>
        </div>
      </div>
    );
  }
}
TransactionJumbotron.propTypes = {
  tx: PropTypes.shape({}).isRequired,
};


export default TransactionJumbotron;
