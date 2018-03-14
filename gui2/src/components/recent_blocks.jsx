import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import api from '../api';
import format from '../utils/format';

import Jumbotron from './jumbotron';
import RecentBlocksJumbotron from './jumbotron_recent_blocks';

const has = Object.prototype.hasOwnProperty;

class RecentBlocks extends Component {
  constructor(props) {
    super(props);
    this.state = {
      recent_blocks: [],
    };
  }

  componentDidMount() {
    const recentBlocks = this.state.recent_blocks;

    function processBlock(block) {
      recentBlocks.push({
        height: block.height,
        mediantime: block.mediantime,
        size: block.size,
        tx_count: block.tx.length,
        hash: block.hash,
        weight: block.weight,
      });
      if (has.call(block, 'previousblockhash')) {
        return block.previousblockhash;
      }
      return null;
    }

    api.getChainInfo()
      .then((data) => {
        let promise = api.getBlockByHash(data.bestblockhash)
          .then(block => block)
          .then(processBlock);

        for (let i = 0; i < 9; i += 1) {
          promise = promise.then((blockhash) => {
            if (blockhash) {
              return api.getBlockByHash(blockhash).then(processBlock);
            }
            return null;
          });
        }
        return promise;
      }).finally(() => {
        this.setState({
          recent_blocks: recentBlocks,
        });
      });
  }

  render() {
    const blocks = this.state.recent_blocks;

    function generateBlocksRows() {
      return blocks.map((block) => {
        const time = format.formatDate(block.mediantime * 1000);
        return (
          <div className="blocks-table-row block-data" key={block.height}>
            <div className="blocks-table-cell"><Link to={`/gui2/block/${block.hash}`}>{block.height}</Link></div>
            <div className="blocks-table-cell">{time}</div>
            <div className="blocks-table-cell">{block.tx_count}</div>
            <div className="blocks-table-cell">{block.size}</div>
            <div className="blocks-table-cell">{block.weight}</div>
          </div>
        );
      });
    }

    return (
      <div>
        <Jumbotron component={RecentBlocksJumbotron} />
        <div className="container">
          <div className="blocks-table">
            <div className="blocks-table-row header">
              <div className="blocks-table-cell">Height</div>
              <div className="blocks-table-cell">Timestamp</div>
              <div className="blocks-table-cell">Transactions</div>
              <div className="blocks-table-cell">Size (KB)</div>
              <div className="blocks-table-cell">Weight (KWU)</div>
            </div>
            {generateBlocksRows()}
          </div>
        </div>
      </div>
    );
  }
}

export default RecentBlocks;
