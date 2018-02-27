import React, { Component } from 'react';
import { render } from 'react-dom';

import Footer from './components/footer.jsx';
import Navbar from './components/navbar.jsx';
import RecentBlocks from './components/recent_blocks.jsx';

class Body extends Component {
    render() {
        return (
          <div className="explorer-container">
            <div class="content-wrap">
              <Navbar />
              <RecentBlocks />
            </div>
            <Footer />
          </div>
        );
    }
}

render(<Body />, document.getElementById('liquid-explorer'));
