import React, { Component } from 'react';
import Randomizer from './components/Randomizer';
import Playlists from './components/Playlists';

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

const getRedisHistory = async (playlist) => {
  let body;
  try {
    const response = await fetch(`/api/redis?user=${playlist.user.toLowerCase()}&list=${playlist.name}`, {
        method: 'POST',
        body: JSON.stringify(playlist),
        headers: new Headers({
          'Content-Type': 'application/json'
        })
      });
    body = await response.json();
  } catch (err) {
    console.error('Error: ', err);
  }
  return body;
}

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: true,
      idCurrentPlaylist: 0
    };

    this.changePlaylist = this.changePlaylist.bind(this);
    this.updateBeverageHistory = this.updateBeverageHistory.bind(this);
  }

  componentDidMount() {
    let playlists;
    getFrontpagePlaylists()
      .then(result => {
        playlists = result.playlists
        return result.playlists.find((elem) => {
          return elem.name.toLowerCase() === 'tgif';
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
    getRedisHistory(playlist)
      .then(newBeverages => {
        playlist.beverages = newBeverages
        this.setState({
          currentPlaylist: playlist
        });
      })
      .catch(err => console.error('Error: ', err));
  };

  updateBeverageHistory(newBeverages){
    let newCurrentPlaylist = this.state.currentPlaylist;
    newCurrentPlaylist.beverages = newBeverages;
    this.setState({
      currentPlaylist: newCurrentPlaylist
    });
  }

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
        <Randomizer playlist={this.state.currentPlaylist} updateBeverages={this.updateBeverageHistory}/>
        <Playlists playlists={this.state.playlists} onClick={this.changePlaylist} />
      </div>
    );
  }
}

export default App;
