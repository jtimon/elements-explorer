import React from 'react';
import PropTypes from 'prop-types';

import dom from '../utils/dom';
import format from '../utils/format';

function VOut({ showAdvanced, vout }) {
  const { scriptpubkey_type } = vout;
  const isPegOut = 'pegout_scriptpubkey_type' in vout;
  const isConfidential = 'ct_bits' in vout;

  let voutBody = null;
  if (!isPegOut && scriptpubkey_type !== 'fee') {
    voutBody = (
      <div className={dom.classNames('vout-body', dom.showIf(showAdvanced))}>
        <div>
          <div>Type</div>
          <div>{scriptpubkey_type}</div>
        </div>
        <div>
          <div>scriptPubKey.asm</div>
          <div>{vout.scriptpubkey_asm}</div>
        </div>
        <div>
          <div>scriptPubKey.hex</div>
          <div>{vout.scriptpubkey_hex}</div>
        </div>
        <div>
          <div>Asset</div>
          <div>{vout.asset}</div>
        </div>
      </div>
    );
  } else if (isPegOut && vout.pegout_scriptpubkey_type !== 'fee') {
    voutBody = (
      <div className={dom.classNames('vout-body', dom.showIf(showAdvanced))}>
        <div>
          <div>Peg-out Type</div>
          <div>{vout.pegout_scriptpubkey_type}</div>
        </div>
        <div>
          <div>Peg-out ASM</div>
          <div>{vout.pegout_scriptpubkey_asm}</div>
        </div>
        <div>
          <div>Peg-out Hex</div>
          <div>{vout.pegout_scriptpubkey_hex}</div>
        </div>
        <div>
          <div>Asset</div>
          <div>{vout.asset}</div>
        </div>
      </div>
    );
  }

  let header = null;
  if (isPegOut) {
    header = ((vout.pegout_scriptpubkey_addresses) ? (
      <span>{vout.pegout_scriptpubkey_addresses[0]}</span>
    ) : (
      <span>Nonstandard</span>
    ));
  } else if (!vout.scriptpubkey_addresses) {
    header = (<span>{format.capitalizeFirstLetter(scriptpubkey_type)}</span>);
  } else {
    header = (<span>{vout.scriptpubkey_addresses[0]}</span>);
  }

  return (
    <div className={dom.classNames('vout', dom.classIf(isPegOut, 'peg-out'), dom.classIf(showAdvanced, 'active'))}>
      <div className="vout-header">
        <div>
          {header}
          <span>{(isConfidential) ? 'Confidential' : `${Number(Number(vout.value).toFixed(8))} BTC`}</span>
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
