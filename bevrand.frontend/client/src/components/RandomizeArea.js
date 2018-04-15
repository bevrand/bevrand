import React, { Component } from 'react';
import Header from './Header';
import Randomizer from './Randomizer';
import Playlists from './PlaylistSelection';
import TopRolledBeverages from './TopRolledBeverages';

const getFrontpagePlaylists = async () => {
  let body;
  let response;
  try {
    response = await fetch('/api/frontpage');
    body = await response.json();
  } catch (err) {
    console.error('Error: ', err);
  }
  return body;
};

class RandomizeArea extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: true
    };

    this.changePlaylist = this.changePlaylist.bind(this);
  }

  componentDidMount() {
    let playlists;
    console.log(this.props);

    getFrontpagePlaylists()
      .then(result => {
        playlists = result;
        return result.find((elem) => {
          return elem.list.toLowerCase() === 'tgif';
        });
      })
      .then(currentPlaylist => {
        this.setState({
          isLoading: false,
          playlists: playlists,
          currentPlaylist: currentPlaylist
        });
      })
      .catch(err => console.log(err.message));
  }

  changePlaylist(playlist) {
    this.setState({
      currentPlaylist: playlist
    });
  };

  render() {
    if (this.state.isLoading) {
      return (
        <div className="App">
          <p>App is still loading, please wait....</p>
        </div>
      )
    }
    return (
      <div className="RandomizeArea">
      {/* TODO: put these components in a seperate Component, like this:
        https://medium.com/@pshrmn/a-simple-react-router-v4-tutorial-7f23ff27adf */}
      {/* Passing the props (of the main logged in user to the components like so:
        https://github.com/ReactTraining/react-router/issues/5521) */}
        <Header />
        <Randomizer playlist={this.state.currentPlaylist} />
        <Playlists playlists={this.state.playlists} onClick={this.changePlaylist} />
        <TopRolledBeverages playlist={this.state.currentPlaylist} />
      </div>
    );
  }
}

export default RandomizeArea;
