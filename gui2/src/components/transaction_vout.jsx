import React from 'react';
import PropTypes from 'prop-types';

import dom from '../utils/dom';

function VOut({ showAdvanced, vout }) {
  const { scriptPubKey } = vout;
  const { type } = scriptPubKey;
  const isPegOut = 'pegout_type' in scriptPubKey;

  let voutBody = null;
  if (!isPegOut && type !== 'fee') {
    voutBody = (
      <div className={dom.classNames('vout-body', dom.showIf(showAdvanced))}>
        <div>
          <div>Type</div>
          <div>{type}</div>
        </div>
        <div>
          <div>scriptPubKey.hex</div>
          <div>{scriptPubKey.hex}</div>
        </div>
      </div>
    );
  } else if (isPegOut && scriptPubKey.pegout_type !== 'fee') {
    voutBody = (
      <div className={dom.classNames('vout-body', dom.showIf(showAdvanced))}>
        <div>
          <div>Peg-out Type</div>
          <div>{scriptPubKey.pegout_type}</div>
        </div>
        <div>
          <div>Peg-out Hex</div>
          <div>{scriptPubKey.pegout_hex}</div>
        </div>
      </div>
    );
  }

  let header = null;
  if (isPegOut) {
    header = ((scriptPubKey.pegout_addresses) ? (
      <a href="#addr">{scriptPubKey.pegout_addresses[0]}</a>
    ) : (
      <span>Non-standard address</span>
    ));
  } else if (type === 'fee') {
    header = (<span>Fee</span>);
  } else if (['nonstandard', 'true'].includes(type) || !scriptPubKey.addresses) {
    header = (<span>Non-standard address</span>);
  } else {
    header = (<a href="#addr">{scriptPubKey.addresses[0]}</a>);
  }

  return (
    <div className={dom.classNames('vout', dom.classIf(isPegOut, 'peg-out'), dom.classIf(showAdvanced, 'active'))}>
      <div className="vout-header">
        {header}
      </div>
      {voutBody}
    </div>
  );
}
VOut.propTypes = {
  showAdvanced: PropTypes.bool.isRequired,
  vout: PropTypes.shape({}).isRequired,
};

export default VOut;
