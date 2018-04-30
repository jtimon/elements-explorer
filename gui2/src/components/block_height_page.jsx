import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';

import api from '../utils/api';
import utils from '../utils/utils';

import NotFoundPage from './not_found_page';

class BlockHeightPage extends Component {
  constructor(props) {
    super(props);
    this.loadBlock = this.loadBlock.bind(this);
    this.state = {
      loading: true,
      redirect: '',
      returnHome: false,
      notFound: false,
    };
  }

  componentDidMount() {
    this.loadBlock(this.props.match.params.blockheight);
  }

  componentWillReceiveProps(nextProps) {
    this.loadBlock(nextProps.match.params.blockheight);
  }

  loadBlock(blockheight) {
    if (utils.isNaturalNumber(blockheight)) {
      const height = parseInt(blockheight, 10);
      api.getBlockByHeight(height)
        .then((block) => {
          this.setState({
            loading: false,
            redirect: block.hash,
          });
        })
        .catch((err) => {
          const { error } = err;
          if (error && error.message === 'Block height out of range') {
            this.setState({
              loading: false,
              notFound: true,
            });
          }
        });
    } else {
      this.setState({
        loading: false,
        returnHome: true,
      });
    }
  }

  render() {
    const {
      loading, notFound, redirect, returnHome,
    } = this.state;
    if (loading) {
      return (
        <div className="container loading-page">
          <img alt="" src="/static/img/Loading.gif" />
        </div>
      );
    } else if (notFound) {
      return (
        <NotFoundPage />
      );
    } else if (returnHome) {
      return (
        <Redirect to="/" />
      );
    }
    return (redirect ? (
      <Redirect to={`/block/${redirect}`} />
    ) : null);
  }
}
BlockHeightPage.propTypes = {
  match: PropTypes.shape({
    isExact: PropTypes.bool,
    params: PropTypes.object.isRequired,
    path: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
  }).isRequired,
};

export default BlockHeightPage;
