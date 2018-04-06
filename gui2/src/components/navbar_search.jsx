import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import api from '../utils/api';
import format from '../utils/format';
import utils from '../utils/utils';

class NavbarSearch extends Component {
  static handleSubmit(event) {
    event.preventDefault();
    const input = event.target.querySelector('#search-input');
    const value = format.trim(input.value.toLowerCase());
    NavbarSearch.search(value);
  }

  static search(str) {
    if (utils.isNaturalNumber(str)) {
      store.dispatchMerge({
        search_redirect: `/gui2/block-height/${str}`,
      });
    } else if (utils.isValidHash(str)) {
      api.getTransaction(str)
        .then((tx) => {
          store.dispatchMerge({
            search_redirect: `/gui2/tx/${tx.txid}`,
          });
        })
        .catch(() => {
          api.getBlockByHash(str)
            .then((block) => {
              store.dispatchMerge({
                search_redirect: `/gui2/block/${block.hash}`,
              });
            });
        });
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.searchRedirect) {
      store.dispatchMerge({
        search_redirect: '',
      });
    }
  }

  render() {
    const { searchRedirect } = this.props;
    return (searchRedirect) ? (
      <Redirect to={searchRedirect} />
    ) : (
      <form className="form-inline" onSubmit={NavbarSearch.handleSubmit}>
        <div className="search-bar">
          <input
            className="form-control search-bar-input"
            id="search-input"
            type="search"
            placeholder="Search for block height, hash, tx, address, etc"
            aria-label="Search"
          />
          <input className="search-bar-submit" type="image" name="submit" src="/gui2/static/img/icons/search.svg" border="0" alt="Submit" />
        </div>
      </form>
    );
  }
}
NavbarSearch.propTypes = {
  searchRedirect: PropTypes.string.isRequired,
};

const mapStateToProps = state => ({
  searchRedirect: state.search_redirect,
});

export default connect(mapStateToProps)(NavbarSearch);
