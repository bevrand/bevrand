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
    const response = await fetch(`/api/redis?user=${playlist.user.toLowerCase()}&list=${playlist.name}`);
    body = await response.json();
  } catch (err) {
    console.error('Error: ', err);
  }
  return body;
}

const mergeRedisData = (currentPlaylist, redisHistory) => {
  const redisArrayName = `${currentPlaylist.user.toLowerCase()}:${currentPlaylist.name}`;
  currentPlaylist.beverages = currentPlaylist.beverages.map(beverage => {
    const matchedElem = redisHistory[redisArrayName].find(elem => {
      return elem.drink === beverage;
    });
    const rolled = matchedElem ? matchedElem.rolled : 0;
    return { drink: beverage, rolled: rolled };
  });
  return currentPlaylist;
}

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: true,
      idCurrentPlaylist: 0
    };

    this.changePlaylist = this.changePlaylist.bind(this);
  }

  componentDidMount() {
    let playlists;
    let currentPlaylist;
    getFrontpagePlaylists()
      .then(result => {
        playlists = result.playlists
        return result.playlists.find((elem) => {
          return elem.name.toLowerCase() === 'tgif';
        });
      })
      .then(retrievedPlaylist => {
        currentPlaylist = retrievedPlaylist;
        return getRedisHistory(retrievedPlaylist);
      })
      .then(redisHistory => {
        currentPlaylist = mergeRedisData(currentPlaylist, redisHistory);
        console.log(currentPlaylist);
        this.setState({
          isLoading: false,
          playlists: playlists,
          currentPlaylist: currentPlaylist
        });
      })
      .catch(err => console.log(err.message));
  }

  changePlaylist(playlist) {
    //TODO: Retrieve redis history for the playlist, on every change of playlist
    let newPlaylist;
    getRedisHistory(playlist)
      .then(redisHistory => {
        newPlaylist = mergeRedisData(playlist, redisHistory);
        this.setState({
          currentPlaylist: newPlaylist
        });
      })
      .catch(err => console.error('Error: ', err));
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
      </div>
    );
  }
}

export default App;
