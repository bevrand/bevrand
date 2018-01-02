import React from 'react';
import ReactDOM from 'react-dom';
// import 'bootstrap/dist/css/bootstrap.css';
// import 'font-awesome/css/font-awesome.css';
// Check if magnific-popup css is needed
// import './index.css';
import './original-scss/combinedStyles.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<App />, document.getElementById('randomize-area'));
registerServiceWorker();
