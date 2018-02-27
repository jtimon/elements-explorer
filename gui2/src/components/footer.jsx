import React, { Component } from 'react';
import { render } from 'react-dom';

class Footer extends Component {
    render() {
        return (
          <footer className="footer">
            <div className="container">
              <span>&copy; Blockstream  Corp. All rights reserved.</span>
              <span>Code at <a href="#">GitHub</a></span>
            </div>
          </footer>
        );
    }
}

export default Footer;
