import React, { Component } from 'react';
import { render } from 'react-dom';
import { BrowserRouter } from 'react-router-dom'
import { Route, Switch } from 'react-router';

import Footer from './components/footer.jsx';
import Navbar from './components/navbar.jsx';
import RecentBlocks from './components/recent_blocks.jsx';
import BlockPage from './components/block_page.jsx';

class Body extends Component {
    render() {
        return (
          <div className="explorer-container">
            <div className="content-wrap">
              <Navbar />
              <BrowserRouter>
                <Switch>
                  <Route exact path="/gui2/" component={RecentBlocks}/>
                  <Route path="/gui2/block/:blockhash" component={BlockPage}/>
                </Switch>
              </BrowserRouter>
            </div>
            <Footer />
          </div>
        );
    }
}

render(<Body />, document.getElementById('liquid-explorer'));
