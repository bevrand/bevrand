import React, { Component } from 'react';
import Randomizer from './components/Randomizer';
import Playlists from './components/Playlists';

class App extends Component {
  constructor(props){
    super(props);

    this.state = {
      isLoading: true,
      idCurrentPlaylist: 0
    };

    this.changePlaylist = this.changePlaylist.bind(this);
  }

  componentDidMount(){
    this.getFrontpagePlaylists()
      .then(res => {
        const currentPlaylist = res.playlists.find((elem) => {
          return elem.name.toLowerCase() === 'tgif';
        });

        this.setState({
          isLoading: false,
          playlists: res.playlists,
          currentPlaylist: currentPlaylist
        })
      })
      .catch(err => console.log(err.message));
  }

  getFrontpagePlaylists = async () => {
    const response = await fetch('/api/frontpagelists');
    const body = await response.json();

    if(response.status !== 200) throw Error(body.message);

    return body;
  };

  getRedisHistory = async (playlist) => {
    const response = await fetch(`/api/redis/user=${playlist.user}&list=${playlist.name}`);
    const body = await response.json();

    return body;
  }

  changePlaylist(playlist){
    //TODO: Retrieve redis history for the playlist, on every change of playlist
    const newPlaylist = playlist;
    this.setState({
      currentPlaylist: newPlaylist
    });
  };

  render() {
    if(this.state.isLoading){
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
