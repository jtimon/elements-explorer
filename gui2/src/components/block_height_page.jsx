import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';

import api from '../utils/api';

class BlockHeightPage extends Component {
  constructor(props) {
    super(props);
    this.loadBlock = this.loadBlock.bind(this);
    this.state = {
      redirect: '',
    };
  }

  componentDidMount() {
    this.loadBlock(this.props.match.params.blockheight);
  }

  componentWillReceiveProps(nextProps) {
    this.loadBlock(nextProps.match.params.blockheight);
  }

  loadBlock(blockheight) {
    api.getBlockByHeight(blockheight)
      .then((block) => {
        this.setState({
          redirect: block.hash,
        });
      });
  }

  render() {
    const { redirect } = this.state;
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
