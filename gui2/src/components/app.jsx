import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Route, Switch } from 'react-router';

import Footer from './footer';
import Navbar from './navbar';
import RecentBlocks from './recent_blocks';
import BlockPage from './block_page';
import BlockHeightPage from './block_height_page';
import TransactionPage from './transaction_page';

function App() {
  return (
    <BrowserRouter>
      <div className="explorer-container">
        <div className="content-wrap">
          <Navbar />
          <Switch>
            <Route exact path="/" component={RecentBlocks} />
            <Route path="/block/:blockhash" component={BlockPage} />
            <Route path="/block-height/:blockheight" component={BlockHeightPage} />
            <Route path="/tx/:txid" component={TransactionPage} />
          </Switch>
        </div>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
