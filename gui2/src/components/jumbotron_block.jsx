import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import format from '../utils/format';

import JumbotronTooltip from './jumbotron_tooltip';

class BlockJumbotron extends Component {
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
    const { block, chainInfo } = this.props;
    const blockHeight = (typeof block.height !== 'undefined') ? format.formatNumber(block.height) : '';
    const previousBlock = block.previousblockhash;
    const nextBlock = (typeof chainInfo.blocks !== 'undefined' && typeof block.height !== 'undefined') ?
      chainInfo.blocks !== block.height : false;
    const { showCodeTooltip } = this.state;
    const tooltipData = {
      hash: block.hash,
      size: block.size,
      height: block.height,
      version: block.version,
      merkleroot: block.merkleroot,
      tx: block.tx,
      time: block.time,
      nonce: block.nonce,
      bits: block.bits,
    };
    if (previousBlock) {
      tooltipData.previousblockhash = previousBlock;
    }

    return (
      <div className="container">
        <h1>Block {blockHeight}</h1>
        <div className="block-hash">
          <span>{(block.hash) ? block.hash : ''}</span>
          {(block.hash) ? (
            <JumbotronTooltip
              showCodeTooltip={showCodeTooltip}
              clickHandler={this.handleMouseClick}
              clickCloseHandler={this.handleMouseClickClose}
              header={`Block ${blockHeight}`}
              data={tooltipData}
            />
          ) : null}
        </div>
        <div className="prev-next-blocks-btns">
          <div>
            <div>
              {(previousBlock) ? (
                <Link to={`/gui2/block/${previousBlock}`}>
                  <div>
                    <div>
                      <img alt="" src="/gui2/static/img/icons/Arrow-left-blue.svg" />
                    </div>
                    <div>
                      <span>Previous</span>
                    </div>
                  </div>
                </Link>
              ) : null}
            </div>
          </div>
          <div>
            {(nextBlock) ? (
              <Link to={`/gui2/block-height/${block.height + 1}`}>
                <div>
                  <div>
                    <span>Next</span>
                  </div>
                  <div>
                    <img alt="" src="/gui2/static/img/icons/Arrow-r-blue.svg" />
                  </div>
                </div>
              </Link>
            ) : null}
          </div>
        </div>
      </div>
    );
  }
}
BlockJumbotron.propTypes = {
  block: PropTypes.shape({}).isRequired,
  chainInfo: PropTypes.shape({}).isRequired,
};

const mapStateToProps = state => ({
  chainInfo: state.chainInfo,
});

export default connect(mapStateToProps)(BlockJumbotron);
