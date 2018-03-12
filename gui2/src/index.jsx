import React, { Component } from 'react';
import { render } from 'react-dom';
import { BrowserRouter } from 'react-router-dom'
import { Route, Switch } from 'react-router';

import Footer from './components/footer.jsx';
import Navbar from './components/navbar.jsx';
import RecentBlocks from './components/recent_blocks.jsx';
import BlockPage from './components/block_page.jsx';
import TransactionPage from './components/transaction_page.jsx';

class Body extends Component {
    render() {
        return (
          <BrowserRouter>
          <div className="explorer-container">
            <div className="content-wrap">
              <Navbar />
              <Switch>
                <Route exact path="/gui2/" component={RecentBlocks}/>
                <Route path="/gui2/block/:blockhash" component={BlockPage}/>
                <Route path="/gui2/tx/:txid" component={TransactionPage}/>
              </Switch>
            </div>
            <Footer />
          </div>
          </BrowserRouter>
        );
    }
}

render(<Body />, document.getElementById('liquid-explorer'));
