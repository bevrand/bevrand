import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import RandomizeArea from './components/RandomizeArea';
import Login from './components/Login';
import SignUp from './components/SignUp';
import AuthService from './components/AuthService';
import withAuth from './components/withAuth';
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
    Auth.logout();
    this.props.history.replace('/login');
  }

  render() {
    return (
      <div className="App">
        <Navigation onLogout={this.handleLogout} />
        {/* TODO: create high order component for randomizer (user) */}
        <Route exact path="/" component={RandomizeArea} />
        <Route path="/user" component={withAuth(RandomizeArea)} />
        <Route path="/login" component={Login} />
        <Route path="/register" component={SignUp} />
      </div>
    );
  }
}

export default App;
