import React, { Component } from 'react';
import { render } from 'react-dom';

class Body extends Component {
    render(){
        return (
          <div className="explorer-container">
            <nav className="navbar">
              <div className="container">
                <a className="navbar-brand" href="#">
                  <img src="/gui2/static/img/icons/Menu-logo.svg" height="50" className="d-inline-block align-top" alt="" />
                </a>
              </div>
            </nav>
            <div className="jumbotron jumbotron-fluid">
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
            </div>
            <div className="container">
              <div className="blocks-table">
                <div className="blocks-table-row header">
                  <div className="blocks-table-cell">Heightasdfasdf</div>
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
            <footer className="footer">
              <div className="container">
                <span>&copy; Blockstream  Corp. All rights reserved.</span>
                <span>Code at <a href="#">GitHub</a></span>
              </div>
            </footer>
          </div>
        );
    }
}

render(<Body />, document.getElementById('liquid-explorer'));
