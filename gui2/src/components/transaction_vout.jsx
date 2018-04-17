import React from 'react';
import PropTypes from 'prop-types';

import dom from '../utils/dom';
import format from '../utils/format';

function VOut({ showAdvanced, vout }) {
  const { scriptPubKey } = vout;
  const { type } = scriptPubKey;
  const isPegOut = 'pegout_type' in scriptPubKey;
  const isConfidential = 'ct-bits' in vout;

  let voutBody = null;
  if (!isPegOut && type !== 'fee') {
    voutBody = (
      <div className={dom.classNames('vout-body', dom.showIf(showAdvanced))}>
        <div>
          <div>Type</div>
          <div>{type}</div>
        </div>
        <div>
          <div>scriptPubKey.asm</div>
          <div>{scriptPubKey.asm}</div>
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
          <div>Peg-out ASM</div>
          <div>{scriptPubKey.pegout_asm}</div>
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
      <span>Nonstandard</span>
    ));
  } else if (!scriptPubKey.addresses) {
    header = (<span>{format.capitalizeFirstLetter(type)}</span>);
  } else {
    header = (<a href="#addr">{scriptPubKey.addresses[0]}</a>);
  }

  return (
    <div className={dom.classNames('vout', dom.classIf(isPegOut, 'peg-out'), dom.classIf(showAdvanced, 'active'))}>
      <div className="vout-header">
        <div>
          {header}
          <span>{(isConfidential) ? 'Confidential' : `${vout.value} BTC`}</span>
        </div>
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
