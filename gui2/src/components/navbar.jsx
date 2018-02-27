import React, { Component } from 'react';
import { render } from 'react-dom';

class Navbar extends Component {
    render() {
        return (
          <nav className="navbar">
            <div className="container">
              <a className="navbar-brand" href="#">
                <img src="/gui2/static/img/icons/Menu-logo.svg" height="50" className="d-inline-block align-top" alt="" />
              </a>
            </div>
          </nav>
        );
    }
}

export default Navbar;
