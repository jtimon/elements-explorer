import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';

import api from '../utils/api';
import utils from '../utils/utils';

class BlockHeightPage extends Component {
  constructor(props) {
    super(props);
    this.loadBlock = this.loadBlock.bind(this);
    this.state = {
      redirect: '',
      returnHome: false,
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
            redirect: block.hash,
          });
        });
    } else {
      this.setState({
        returnHome: true,
      });
    }
  }

  render() {
    const { redirect, returnHome } = this.state;
    if (returnHome) {
      return (
        <Redirect to="/gui2/" />
      );
    }
    return (redirect ? (
      <Redirect to={`/gui2/block/${redirect}`} />
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
