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
        return (
          <div>
            <Jumbotron component={(props) => (
                <BlockJumbotron block={block} />
            )} pageType={'block-page'} />
            <div className="container">
              <p>This block: {block.hash}</p>
            </div>
          </div>
        );
    }
}

export default BlockPage;
