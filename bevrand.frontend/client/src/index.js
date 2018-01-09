import React from 'react';
import ReactDOM from 'react-dom';
//TODO: add other javascript to this bundler

import './original-scss/combinedStyles.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<App />, document.getElementById('randomize-area'));
registerServiceWorker();
