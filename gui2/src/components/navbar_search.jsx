import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import api from '../utils/api';
import format from '../utils/format';
import utils from '../utils/utils';

class NavbarSearch extends Component {
  static search(str) {
    if (utils.isNaturalNumber(str)) {
      store.dispatchMerge({
        searchRedirect: `/block-height/${str}`,
      });
    } else if (utils.isValidHash(str)) {
      api.getTransaction(str)
        .then((tx) => {
          store.dispatchMerge({
            searchRedirect: `/tx/${tx.txid}`,
          });
        })
        .catch(() => {
          api.getBlockByHash(str)
            .then((block) => {
              store.dispatchMerge({
                searchRedirect: `/block/${block.hash}`,
              });
            });
        });
    }
  }

  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.searchRedirect) {
      store.dispatchMerge({
        searchRedirect: '',
      });
    }
  }

  handleSubmit(event) {
    event.preventDefault();
    const value = format.trim(this.searchInput.value.toLowerCase());
    NavbarSearch.search(value);
  }

  render() {
    const { searchRedirect } = this.props;
    return (searchRedirect) ? (
      <Redirect to={searchRedirect} />
    ) : (
      <form className="form-inline" onSubmit={this.handleSubmit}>
        <div className="search-bar">
          <input
            className="form-control search-bar-input"
            ref={(ref) => { this.searchInput = ref; }}
            type="search"
            placeholder="Search for block height, hash, or tx"
            aria-label="Search"
          />
          <input className="search-bar-submit" type="image" name="submit" src="/static/img/icons/search.svg" border="0" alt="Submit" />
        </div>
      </form>
    );
  }
}
NavbarSearch.propTypes = {
  searchRedirect: PropTypes.string.isRequired,
};

const mapStateToProps = state => ({
  searchRedirect: state.searchRedirect,
});

export default connect(mapStateToProps)(NavbarSearch);
