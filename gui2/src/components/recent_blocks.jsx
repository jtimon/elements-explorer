import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

import api from '../utils/api';
import dom from '../utils/dom';
import format from '../utils/format';
import utils from '../utils/utils';

class RecentBlocks extends Component {
  render() {
    const {
      blocks, chainInfo, loadBlocks, loading,
    } = this.props;
    const bestBlockHash = chainInfo.bestblockhash;
    const hasBlocks = !utils.isEmptyArray(blocks);
    const hasNewer = hasBlocks && blocks[0].hash !== bestBlockHash;
    const hasOlder = hasBlocks && blocks[blocks.length - 1].previousBlockHash;

    function generateBlocksRows() {
      return blocks.map((block) => {
        const time = format.formatDate(block.mediantime * 1000);
        return (
          <div className="blocks-table-row block-data" key={block.height}>
            <div className="blocks-table-cell"><Link to={`/block/${block.hash}`}>{block.height}</Link></div>
            <div className="blocks-table-cell">{time}</div>
            <div className="blocks-table-cell">{block.txCount}</div>
            <div className="blocks-table-cell">{block.size / 1000}</div>
            <div className="blocks-table-cell">{block.weight / 1000}</div>
          </div>
        );
      });
    }

    function handleClickOlder() {
      if (hasOlder) {
        const { previousBlockHash } = blocks[blocks.length - 1];
        loadBlocks(previousBlockHash);
      }
    }

    function handleClickNewer() {
      if (hasNewer) {
        const newestBlock = blocks[0];
        api.getBlockByHeight(newestBlock.height + 10)
          .then((block) => {
            loadBlocks(block.hash);
          });
      }
    }

    return (
      <div className="blocks-table">
        <div className="blocks-table-row header">
          <div className="blocks-table-cell">Height</div>
          <div className="blocks-table-cell">Timestamp</div>
          <div className="blocks-table-cell">Transactions</div>
          <div className="blocks-table-cell">Size (KB)</div>
          <div className="blocks-table-cell">Weight (KWU)</div>
        </div>
        {generateBlocksRows()}
        <div className={dom.classNames('blocks-table-row', 'block-data', 'loading', dom.showIf(loading))}>
          <img alt="" src="/static/img/Loading.gif" />
        </div>
        <div className={dom.classNames('newer-older-blocks-btns', dom.showIf(!loading))}>
          <div>
            <div
              className={dom.classNames('blocks-btn', 'newer-btn', dom.showIf(hasNewer))}
              role="button"
              tabIndex={0}
              onClick={handleClickNewer}
              onKeyPress={handleClickNewer}
            >
              <div>
                <img alt="" src="/static/img/icons/Arrow-left-blue.svg" />
              </div>
              <span>Newer</span>
            </div>
          </div>
          <div>
            <div
              className={dom.classNames('blocks-btn', 'older-btn', dom.showIf(hasOlder))}
              role="button"
              tabIndex={0}
              onClick={handleClickOlder}
              onKeyPress={handleClickOlder}
            >
              <span>Older</span>
              <div>
                <img alt="" src="/static/img/icons/Arrow-r-blue.svg" />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

RecentBlocks.propTypes = {
  blocks: PropTypes.arrayOf(PropTypes.shape({})).isRequired,
  loading: PropTypes.bool.isRequired,
  loadBlocks: PropTypes.func.isRequired,
  chainInfo: PropTypes.shape({
    bestblockhash: PropTypes.string,
  }).isRequired,
};

const mapStateToProps = state => ({
  chainInfo: state.chainInfo,
});

export default connect(mapStateToProps)(RecentBlocks);
