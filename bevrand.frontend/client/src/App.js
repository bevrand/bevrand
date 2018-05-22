import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import RandomizeArea from './components/RandomizeArea';
import Login from './components/Login';
import AuthService from './components/AuthService';
import withAuth from './components/withAuth';
import Register from './components/Register';
import PlaylistCreator from './components/PlaylistCreator';
const Auth = new AuthService();

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      userLoggedIn: true
    };

    this.handleLogout = this.handleLogout.bind(this);
  }

  changePlaylist(playlist) {
    this.setState({
      currentPlaylist: playlist
    });
  };

  handleLogout() {
    console.log('Logging user out');
    Auth.logout();
  }

  render() {
    return (
      <div className="App">
        <Navigation handleLogout={this.handleLogout} />
        <Route exact path="/" component={RandomizeArea} />
        <Route path="/user" component={withAuth(RandomizeArea)} />
        <Route path="/create" component={withAuth(PlaylistCreator)} />
        <Route path="/login" component={Login} />
        <Route path="/register" component={Register} />
      </div>
    );
  }
}

export default App;
