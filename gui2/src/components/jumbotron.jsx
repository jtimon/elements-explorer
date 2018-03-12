import React from 'react';
import PropTypes from 'prop-types';

function Jumbotron({ component, pageType }) {
  const JumbotronComponent = component;
  let classes = 'jumbotron jumbotron-fluid';
  if (pageType) {
    classes += ` ${pageType}`;
  }
  return (
    <div className={classes}>
      {(JumbotronComponent) ? (
        <JumbotronComponent />
      ) : (
        null
      )}
    </div>
  );
}
Jumbotron.defaultProps = {
  component: null,
  pageType: '',
};
Jumbotron.propTypes = {
  component: PropTypes.func,
  pageType: PropTypes.string,
};

export default Jumbotron;
