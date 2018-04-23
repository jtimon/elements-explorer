import React from 'react';
import PropTypes from 'prop-types';

import dom from '../utils/dom';

function JumbotronTooltip({
  showCodeTooltip, clickHandler, clickCloseHandler, header, data,
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
        <img alt="" src="/static/img/icons/code.svg" />
      </div>
      <div className={dom.classNames('overlay', dom.classIf(!showCodeTooltip, 'hide'))} />
      <div className={dom.classNames('code-button-text', dom.classIf(showCodeTooltip, 'active'))}>
        <div
          className="close-button-top"
          role="button"
          tabIndex={0}
          onClick={clickCloseHandler}
          onKeyPress={clickCloseHandler}
        >
          <img alt="" src="/static/img/icons/cancel.svg" />
        </div>
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
            <img alt="" src="/static/img/icons/cancel.svg" />
          </div>
        </div>
      </div>
    </div>
  );
}
JumbotronTooltip.propTypes = {
  showCodeTooltip: PropTypes.bool.isRequired,
  clickHandler: PropTypes.func.isRequired,
  clickCloseHandler: PropTypes.func.isRequired,
  header: PropTypes.string.isRequired,
  data: PropTypes.oneOfType([
    PropTypes.shape({}),
    PropTypes.string,
  ]).isRequired,
};

export default JumbotronTooltip;
