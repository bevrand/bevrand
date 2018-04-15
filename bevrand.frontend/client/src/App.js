import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Header from './components/Header';
import RandomizeArea from './components/RandomizeArea';
import Login from './components/Login';
import Register from './components/Register';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      userLoggedIn: true
    };
  }

  changePlaylist(playlist) {
    this.setState({
      currentPlaylist: playlist
    });
  };

  render() {
    return (
      <div className="App">
        <Navigation />
        <Header />
        <Route exact path="/" component={RandomizeArea} />
        <Route path="/login" component={Login} />
        <Route path="/register" component={Register} />
      </div>
    );
  }
}

export default App;
