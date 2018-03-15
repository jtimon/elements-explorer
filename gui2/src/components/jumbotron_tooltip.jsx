import React from 'react';
import PropTypes from 'prop-types';

import dom from '../utils/dom';

function JumbotronTooltip({
  showTooltip, clickHandler, clickCloseHandler, header, data,
}) {
  return (
    <div className="code-button">
      <div
        className="code-button-btn"
        role="button"
        tabIndex={0}
        onClick={clickHandler}
        onKeyPress={clickHandler}
      >
        <img alt="" src="/gui2/static/img/icons/code.svg" />
      </div>
      <div className={dom.classNames('overlay', dom.classIf(!showTooltip, 'hide'))} />
      <div className={dom.classNames('code-button-text', dom.classIf(showTooltip, 'active'))}>
        <h4>{header}</h4>
        <pre>{JSON.stringify(data, null, 4)}</pre>
        <div
          className="close-button"
          role="button"
          tabIndex={0}
          onClick={clickCloseHandler}
          onKeyPress={clickCloseHandler}
        >
          <div>Close</div>
          <div>
            <img alt="" src="/gui2/static/img/icons/cancel.svg" />
          </div>
        </div>
      </div>
    </div>
  );
}
JumbotronTooltip.propTypes = {
  showTooltip: PropTypes.bool.isRequired,
  clickHandler: PropTypes.func.isRequired,
  clickCloseHandler: PropTypes.func.isRequired,
  header: PropTypes.string.isRequired,
  data: PropTypes.oneOfType([
    PropTypes.shape({}),
    PropTypes.string,
  ]).isRequired,
};

export default JumbotronTooltip;
