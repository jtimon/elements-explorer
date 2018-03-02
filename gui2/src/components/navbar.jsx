import React, { Component } from 'react';
import { render } from 'react-dom';
import { Link } from 'react-router-dom';

class Navbar extends Component {
    render() {
        return (
          <nav className="navbar">
            <div className="container">
              <Link className="navbar-brand" to="/gui2/">
                <img src="/gui2/static/img/icons/Menu-logo.svg" height="50" className="d-inline-block align-top" alt="" />
              </Link>
            </div>
          </nav>
        );
    }
}

export default Navbar;
