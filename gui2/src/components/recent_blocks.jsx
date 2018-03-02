import React, { Component } from 'react';
import { render } from 'react-dom';
import { Link } from 'react-router-dom';

import utils from '../utils.js';

import Jumbotron from './jumbotron.jsx';
import RecentBlocksJumbotron from './jumbotron_recent_blocks.jsx';

class RecentBlocks extends Component {
    constructor(props) {
      super(props);
        this.state = {
          recent_blocks: []
        };
    }

    componentDidMount() {
        function processBlock(block) {
            recentBlocks.push({
                'height': block['height'],
                'mediantime': block['mediantime'],
                'size': block['size'],
                'tx_count': block['tx'].length,
                'hash': block['hash'],
                'weight': block['weight']
            });
            if (block.hasOwnProperty('previousblockhash')) {
                return block['previousblockhash'];
            }
            return null;
        }

        let recentBlocks = this.state.recent_blocks;
        utils.apiChainInfo()
        .then((data) => {
            let promise = utils.apiGetBlockByHash(data.bestblockhash)
                .then((block) => {
                    return block;
                })
                .then(processBlock);

            for (var i = 0; i < 9; i++) {
                promise = promise.then((blockhash) => {
                  if (blockhash) {
                      return utils.apiGetBlockByHash(blockhash).then(processBlock);
                  }
                  return null;
                });
            }
            return promise;
        }).finally(() => {
            this.setState({
              recent_blocks: recentBlocks
            });
        });
    }

    render() {
        function generateBlocksRows() {
            return blocks
              .map((block) => {
                let time = new Date(block.mediantime * 1000);
                return (
                  <div className="blocks-table-row block-data" key={block.height}>
                    <div className="blocks-table-cell"><Link to={'/block/' + block.hash}>{block.height}</Link></div>
                    <div className="blocks-table-cell">{time.toString()}</div>
                    <div className="blocks-table-cell">{block.tx_count}</div>
                    <div className="blocks-table-cell">{block.size}</div>
                    <div className="blocks-table-cell">{block.weight}</div>
                  </div>
              )});
        }
        let blocks = this.state.recent_blocks;
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
