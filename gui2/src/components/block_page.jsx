import React, { Component } from 'react';
import { render } from 'react-dom';

import utils from '../utils.js';

import Jumbotron from './jumbotron.jsx';
import BlockJumbotron from './jumbotron_block.jsx';

class BlockPage extends Component {
    render() {
        const blockhash = this.props.match.params.blockhash;
        return (
          <div>
            <Jumbotron component={BlockJumbotron} />
            <div className="container">
              {blockhash}
            </div>
          </div>
        );
    }
}

export default BlockPage;
