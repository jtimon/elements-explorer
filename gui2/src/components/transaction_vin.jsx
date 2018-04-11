import React from 'react';
import PropTypes from 'prop-types';

import dom from '../utils/dom';

function VIn({
  index, showAdvanced, transaction, vin,
}) {
  const storeTxs = store.getState().transactions;

  if (vin.pegin) {
    return (
      <div className="vin">
        <div className="vin-header">Bitcoin address</div>
      </div>
    );
  } else if (vin.coinbase) {
    return (
      <div className="vin">
        <div className="vin-header">Coinbase</div>
      </div>
    );
  }
  const tx = storeTxs[vin.txid].vout[vin.vout];
  const { scriptSig } = transaction.vin[index];
  const { type } = tx.scriptPubKey;
  const vinBody = (
    <div className={dom.classNames('vin-body', dom.showIf(showAdvanced))}>
      <div>
        <div>scriptSig.ASM</div>
        <div>{scriptSig.asm}</div>
      </div>
      <div>
        <div>scriptSig.hex</div>
        <div>{scriptSig.hex}</div>
      </div>
    </div>
  );

  let header = null;
  if (type === 'nonstandard') {
    header = (<span>Nonstandard</span>);
  } else {
    header = tx.scriptPubKey.addresses.map(addr => (
      <span key={addr}><a href="#addr">{addr}</a></span>
    ));
  }
  return (
    <div key={tx.n} className={dom.classNames('vin', dom.classIf(showAdvanced, 'active'))}>
      <div className="vin-header">
        {header}
      </div>
      {vinBody}
    </div>
  );
}
VIn.propTypes = {
  index: PropTypes.number.isRequired,
  showAdvanced: PropTypes.bool.isRequired,
  transaction: PropTypes.shape({}).isRequired,
  vin: PropTypes.shape({
    coinbase: PropTypes.bool.isRequired,
    txid: PropTypes.string,
    vout: PropTypes.number,
  }).isRequired,
};

export default VIn;
