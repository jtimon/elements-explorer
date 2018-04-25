import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import api from '../utils/api';

import Jumbotron from './jumbotron';
import RecentBlocksJumbotron from './jumbotron_recent_blocks';
import RecentBlocks from './recent_blocks';

const has = Object.prototype.hasOwnProperty;

class RecentBlocksPage extends Component {
  constructor(props) {
    super(props);
    this.loadBlocks = this.loadBlocks.bind(this);
    this.state = {
      recentBlocks: [],
      loading: true,
    };
  }

  componentDidMount() {
    api.getAllChainInformation()
      .then(data => this.loadBlocks(data.bestblockhash))
      .finally(() => {
        this.setState({
          loading: false,
        });
      });
  }

  loadBlocks(bestBlockHash) {
    const recentBlocks = [];

    function processBlock(block) {
      recentBlocks.push({
        height: block.height,
        mediantime: block.mediantime,
        size: block.size,
        txCount: block.tx.length,
        hash: block.hash,
        weight: block.weight,
        previousBlockHash: block.previousblockhash,
      });
      if (has.call(block, 'previousblockhash')) {
        return block.previousblockhash;
      }
      return null;
    }

    let promise = api.getBlockByHash(bestBlockHash)
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

    promise.then(() => {
      this.setState({
        recentBlocks,
      });
    });

    return promise;
  }

  render() {
    const { loading, recentBlocks } = this.state;
    const bestBlockHash = this.props.chainInfo.bestblockhash;

    return (
      <div>
        <Jumbotron component={RecentBlocksJumbotron} />
        <div className="container">
          <RecentBlocks
            blocks={recentBlocks}
            loading={loading}
            bestBlockHash={bestBlockHash}
            loadBlocks={this.loadBlocks}
          />
        </div>
      </div>
    );
  }
}
RecentBlocksPage.propTypes = {
  chainInfo: PropTypes.shape({
    bestblockhash: PropTypes.string,
  }).isRequired,
};

const mapStateToProps = state => ({
  chainInfo: state.chainInfo,
});

export default connect(mapStateToProps)(RecentBlocksPage);
