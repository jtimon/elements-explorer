import React, { Component } from 'react';
import { render } from 'react-dom';

class Jumbotron extends Component {
    render() {
        let JumbotronComponent = this.props.component;
        let pageType = this.props.pageType;
        let classes = "jumbotron jumbotron-fluid";
        if (pageType) {
          classes += ' ' + pageType;
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
}

export default Jumbotron;
