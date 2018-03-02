import React, { Component } from 'react';
import { render } from 'react-dom';

import utils from '../utils.js';

import Jumbotron from './jumbotron.jsx';
import BlockJumbotron from './jumbotron_block.jsx';

class BlockPage extends Component {
    constructor(props) {
      super(props);
        this.state = {
          block: {},
        };
    }

    componentDidMount() {
        utils.apiGetBlockByHash(this.props.match.params.blockhash)
        .then((block) => {
            this.setState({
              block: block
            });
        });
    }

    componentWillReceiveProps(nextProps) {
        utils.apiGetBlockByHash(nextProps.match.params.blockhash)
        .then((block) => {
            this.setState({
              block: block
            });
        });
    }

    render() {
        let block = this.state.block;
        let time = new Date(block.mediantime * 1000);
        return (
          <div>
            <Jumbotron component={(props) => (
                <BlockJumbotron block={block} />
            )} pageType={'block-page'} />
            <div className="container">
              <div className="block-stats-table">
                <div>
                  <div>Height</div>
                  <div>{block.height}</div>
                </div>
                <div>
                  <div>Confirmations</div>
                  <div>{block.confirmations}</div>
                </div>
                <div>
                  <div>Timestamp</div>
                  <div>{time.toString()}</div>
                </div>
                <div>
                  <div>Size (KB)</div>
                  <div>{block.size}</div>
                </div>
                <div>
                  <div>Weight (KWU)</div>
                  <div>{block.weight}</div>
                </div>
                <div>
                  <div>Version</div>
                  <div>{block.version}</div>
                </div>
              </div>
            </div>
          </div>
        );
    }
}

export default BlockPage;
