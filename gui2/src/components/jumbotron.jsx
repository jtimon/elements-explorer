import React, { Component } from 'react';
import { render } from 'react-dom';

class Jumbotron extends Component {
    render() {
        let JumbotronComponent = this.props.component;
        return (
          <div className="jumbotron jumbotron-fluid">
            {(JumbotronComponent) ? (
              <JumbotronComponent />
            ) : (
              null
            )}
          </div>
        );
    }
}

export default Jumbotron;
