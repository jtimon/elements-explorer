import React from 'react';
import { Link } from 'react-router-dom';

import NavbarSearch from './navbar_search';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="container">
        <Link className="navbar-brand" to="/">
          <img src="/static/img/icons/Menu-logo.svg" height="50" className="d-inline-block align-top" alt="" />
        </Link>
        <NavbarSearch />
      </div>
    </nav>
  );
}

export default Navbar;
