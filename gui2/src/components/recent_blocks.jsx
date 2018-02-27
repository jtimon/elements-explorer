import React, { Component } from 'react';
import { render } from 'react-dom';

import Jumbotron from './jumbotron.jsx';

class RecentBlocks extends Component {
    render() {
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
                <div className="blocks-table-row block-data">
                  <div className="blocks-table-cell"><a href="#">507278</a></div>
                  <div className="blocks-table-cell">Fri, 12 Feb 2018 15:35:29 PST</div>
                  <div className="blocks-table-cell">1867</div>
                  <div className="blocks-table-cell">1,034.36</div>
                  <div className="blocks-table-cell">3,992.86</div>
                </div>
                <div className="blocks-table-row block-data">
                  <div className="blocks-table-cell"><a href="#">507278</a></div>
                  <div className="blocks-table-cell">Fri, 12 Feb 2018 15:35:29 PST</div>
                  <div className="blocks-table-cell">1867</div>
                  <div className="blocks-table-cell">1,034.36</div>
                  <div className="blocks-table-cell">3,992.86</div>
                </div>
              </div>
            </div>
          </div>
        );
    }
}

export default RecentBlocks;
