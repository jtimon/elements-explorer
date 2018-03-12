import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

import format from '../utils/format';

function BlockJumbotron({ block }) {
  const blockHeight = (block.height) ? format.formatNumber(block.height) : '';
  const previousBlock = block.previousblockhash;
  const nextBlock = block.nextblockhash;
  return (
    <div className="container">
      <h1>Block {blockHeight}</h1>
      <p className="block-hash">{block.hash} <img alt="" src="/gui2/static/img/icons/code.svg" /></p>
      <div className="prev-next-blocks-btns">
        <div>
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
        </div>
        <div>
          <Link to={`/gui2/block/${nextBlock}`}>
            <div>
              <div>
                <span>Next</span>
              </div>
              <div>
                <img alt="" src="/gui2/static/img/icons/Arrow-r-blue.svg" />
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}
BlockJumbotron.propTypes = {
  block: PropTypes.object.isRequired,
};

export default BlockJumbotron;
