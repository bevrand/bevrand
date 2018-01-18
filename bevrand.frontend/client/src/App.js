import React, { Component } from 'react';
import Randomizer from './components/randomizer';
import Playlists from './components/playlists';

class App extends Component {


  constructor(props){
    super(props);

    // this.playlists = this.getFrontpagePlaylists()

    this.state = {
      currentPlaylist: 0, //TODO: make the default the TGIF playlist, with find function to retrieve key of this playlist
      playlists: {}
    };

    this.changePlaylist = this.changePlaylist.bind(this);
  }

  componentDidMount(){
    this.getFrontpagePlaylists()
      .then(res => {
        this.setState({ playlists: res.playlists })
      })
      .catch(err => console.log(err));
  }

  getFrontpagePlaylists = async () => {
    const response = await fetch('/api/frontpagelists');
    const body = await response.json();

    if(response.status !== 200) throw Error(body.message);

    return body;
  }

  changePlaylist(id){
    this.setState({
      currentPlaylist: id,
      result: null
    });
  }

  render() {
    const currentPlaylist = this.playlists.find((elem) => {
      return elem.id === this.state.currentPlaylist;
    });

    return (
      <div className="App">
        <Randomizer playlist={currentPlaylist} />
        <Playlists playlists={this.playlists} onClick={this.changePlaylist} />
      </div>
    );
  }
}

export default App;
