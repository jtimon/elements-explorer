import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import dom from '../utils/dom';
import format from '../utils/format';

function VIn({
  index, showAdvanced, transaction, vin, transactions, chain,
}) {
  if (vin.pegin) {
    return (
      <div className={dom.classNames('vin', 'peg-in', dom.classIf(showAdvanced, 'active'))}>
        <div className="vin-header">{vin.address}</div>
        <div className={dom.classNames('vin-body', dom.showIf(showAdvanced))}>
          <div>
            <div>txid</div>
            <div>{vin.txid}</div>
          </div>
          <div>
            <div>vout</div>
            <div>{vin.vout}</div>
          </div>
        </div>
      </div>
    );
  } else if (vin.coinbase) {
    return (
      <div className="vin">
        <div className="vin-header">Coinbase</div>
      </div>
    );
  }
  const tx = transactions[chain][vin.txid].vout[vin.vout];
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
  if (!tx.scriptPubKey.addresses) {
    header = (<span>{format.capitalizeFirstLetter(type)}</span>);
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
  chain: PropTypes.string.isRequired,
  transactions: PropTypes.shape({}).isRequired,
};

const mapStateToProps = state => ({
  chain: state.chain,
  transactions: state.transactions,
});

export default connect(mapStateToProps)(VIn);
