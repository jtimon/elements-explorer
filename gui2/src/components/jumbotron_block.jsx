import React, { Component } from 'react';
import { render } from 'react-dom';

import { Link } from 'react-router-dom';

import format from '../utils/format.js';

class BlockJumbotron extends Component {
    render() {
        let block = this.props.block;
        let blockHeight = (block.height) ? format.formatNumber(block.height) : '';
        let previousBlock = block.previousblockhash;
        let nextBlock = block.nextblockhash;
        return (
            <div className="container">
              <h1>Block {blockHeight}</h1>
              <p className="block-hash">{block.hash} <img src="/gui2/static/img/icons/code.svg" /></p>
              <div className="prev-next-blocks-btns">
                <div>
                  <Link to={'/block/' + previousBlock}>
                    <div>
                      <div>
                        <img src="/gui2/static/img/icons/Arrow-left-blue.svg" />
                      </div>
                      <div>
                        <span>Previous</span>
                      </div>
                    </div>
                  </Link>
                </div>
                <div>
                  <Link to={'/block/' + nextBlock}>
                    <div>
                      <div>
                        <span>Next</span>
                      </div>
                      <div>
                        <img src="/gui2/static/img/icons/Arrow-r-blue.svg" />
                      </div>
                    </div>
                  </Link>
                </div>
              </div>
            </div>
        );
    }
}

export default BlockJumbotron;
