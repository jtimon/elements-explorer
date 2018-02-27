import React, { Component } from 'react';
import { render } from 'react-dom';

import Jumbotron from './jumbotron.jsx';

class RecentBlocks extends Component {
    render() {
        function generateBlocksRows() {
            const blocks = [
                {
                    'height': 507278,
                    'timestamp': 'Fri, 12 Feb 2018 15:35:29 PST',
                    'transactions': 1867,
                    'size': '1,034.36',
                    'weight': '3,992.86'
                },
                {
                    'height': 507277,
                    'timestamp': 'Fri, 12 Feb 2018 15:34:20 PST',
                    'transactions': 1726,
                    'size': '1,025.42',
                    'weight': '3,800.34'
                },
                {
                    'height': 507276,
                    'timestamp': 'Fri, 12 Feb 2018 15:33:17 PST',
                    'transactions': 1928,
                    'size': '1,045.21',
                    'weight': '3,999.65'
                }
            ];
            return blocks
              .map((block) => (
                  <div className="blocks-table-row block-data" key={block.height}>
                    <div className="blocks-table-cell"><a href="#">{block.height}</a></div>
                    <div className="blocks-table-cell">{block.timestamp}</div>
                    <div className="blocks-table-cell">{block.transactions}</div>
                    <div className="blocks-table-cell">{block.size}</div>
                    <div className="blocks-table-cell">{block.weight}</div>
                  </div>
              ));
        }
        return (
          <div>
            <Jumbotron />
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
