import React, { Component } from 'react';
import PropTypes from 'prop-types';

import JumbotronTooltip from './jumbotron_tooltip';

class TransactionJumbotron extends Component {
  constructor(props) {
    super(props);
    this.handleMouseClick = this.handleMouseClick.bind(this);
    this.handleMouseClickClose = this.handleMouseClickClose.bind(this);
    this.state = {
      show_code_tooltip: false,
    };
  }

  handleMouseClick() {
    this.setState({
      show_code_tooltip: !this.state.show_code_tooltip,
    });
  }

  handleMouseClickClose() {
    this.setState({
      show_code_tooltip: false,
    });
  }

  render() {
    const { tx } = this.props;
    const tooltipData = tx.hex;
    const showTooltip = this.state.show_code_tooltip;
    return (
      <div className="container">
        <h1>Transaction</h1>
        <div className="block-hash">
          <span>{(tx.txid) ? tx.txid : ''}</span>
          {(tx.txid) ? (
            <JumbotronTooltip
              showTooltip={showTooltip}
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
