import React, { Component } from 'react';
import Randomizer from './components/Randomizer';
import Playlists from './components/Playlists';
import TopRolledBeverages from './components/TopRolledBeverages';

const getFrontpagePlaylists = async () => {
  let body;
  try {
    const response = await fetch('/api/frontpagelists');
    body = await response.json();
  } catch (err) {
    console.error('Error: ', err);
  }
  return body;
};

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: true
    };

    this.changePlaylist = this.changePlaylist.bind(this);
  }

  componentDidMount() {
    let playlists;
    getFrontpagePlaylists()
      .then(result => {
        playlists = result.playlists
        return result.playlists.find((elem) => {
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
      <div className="App">
        <Randomizer playlist={this.state.currentPlaylist} />
        <Playlists playlists={this.state.playlists} onClick={this.changePlaylist} />
        <TopRolledBeverages playlist={this.state.currentPlaylist} />
      </div>
    );
  }
}

export default App;
