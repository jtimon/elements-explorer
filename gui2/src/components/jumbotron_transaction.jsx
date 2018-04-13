import React, { Component } from 'react';
import PropTypes from 'prop-types';

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
    return (
      <div className="container">
        <h1>Transaction</h1>
        <div className="block-hash">
          <span>{(tx.txid) ? tx.txid : ''}</span>
          {(tx.txid) ? (
            <JumbotronTooltip
              showCodeTooltip={showCodeTooltip}
              clickHandler={this.handleMouseClick}
              clickCloseHandler={this.handleMouseClickClose}
              header={`Transaction ${tx.txid}`}
              data={tooltipData}
            />
          ) : null}
        </div>
      </div>
    );
  }
}
TransactionJumbotron.propTypes = {
  tx: PropTypes.shape({}).isRequired,
};


export default TransactionJumbotron;
