import React, { Component } from 'react';
import { render } from 'react-dom';

class RecentBlocksJumbotron extends Component {
    render() {
        return (
            <div className="container">
              <h1>Recent Blocks</h1>
              <div className="block-dropdowns">
                <div className="date-dropdown">
                  <div>
                    <img src="/gui2/static/img/icons/calendar.svg" />
                  </div>
                  <div>
                    <span>Feb 12, 2018</span>
                  </div>
                  <div>
                    <img src="/gui2/static/img/icons/Arrow-down.svg" />
                  </div>
                </div>
                <div className="time-dropdown">
                  <div>
                    <img src="/gui2/static/img/icons/time.svg" />
                  </div>
                  <div>
                    <span>12:00 - 16:00</span>
                  </div>
                  <div>
                    <img src="/gui2/static/img/icons/Arrow-down.svg" />
                  </div>
                </div>
              </div>
            </div>
        );
    }
}

export default RecentBlocksJumbotron;
