import React, { Component } from 'react';
import Randomizer from './components/randomizer';
import Playlists from './components/playlists';

let playlistData = [
  {
    id: 0,
    name: "Girls night out",
    fullImageUrl: "img/portfolio/fullsize/Girls night out - small.jpg",
    thumbImageUrl: "img/portfolio/thumbnails/Girls night out - small.jpg",
    beverages: [
      "melk",
      "bier",
      "wijn",
      "fruitsapje"
    ]
  },
  {
    id: 1,
    name: "Highland Games",
    fullImageUrl: "img/portfolio/fullsize/Highland Games - small.jpg",
    thumbImageUrl: "img/portfolio/thumbnails/Highland Games - small.jpg",
    beverages: [
      "Palm",
      "Tripel",
      "wijn",
      "fruitsapje"
    ]
  },
  {
    id: 2,
    name: "Mancave mayhem",
    fullImageUrl: "img/portfolio/fullsize/Mancave mayhem - small.jpg",
    thumbImageUrl: "img/portfolio/thumbnails/Mancave mayhem - small.jpg",
    beverages: [
      "Champagne",
      "Rode wijn",
      "Witte wijn"
    ]
  },
  {
    id: 3,
    name: "Office madness",
    fullImageUrl: "img/portfolio/fullsize/Office madness - small.jpg",
    thumbImageUrl: "img/portfolio/thumbnails/Office madness - small.jpg",
    beverages: [
      "1",
      "2",
      "3",
      "4",
      "5",
      "6"
    ]
  },
  {
    id: 4,
    name: "Thank god it's friday",
    fullImageUrl: "img/portfolio/fullsize/Thank god it's friday - small.jpg",
    thumbImageUrl: "img/portfolio/thumbnails/Thank god it's friday - small.jpg",
    beverages: [
      "1",
      "2",
      "3",
      "4",
      "5",
      "6"
    ]
  },
  {
    id: 5,
    name: "Happy Holidays",
    fullImageUrl: "img/portfolio/fullsize/The most wonderful time - small.jpg",
    thumbImageUrl: "img/portfolio/thumbnails/The most wonderful time - small.jpg",
    beverages: [
      "1",
      "2",
      "3",
      "4",
      "5",
      "6"
    ]
  }
];

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
      .then(res => this.setState({ playlists: res.playlists }))
      .catch(err => console.log(err));
  }

  getFrontpagePlaylists = async () => {
    const response = await fetch('/api/frontpagelists');
    const body = await response.json();

    if(response.status !== 200) throw Error(body.message);

    return body;
  }

  // componentWillMount(){
  //   const retrievedPlaylists = playlistData;
  //
  //   // Set the current set of Playlists
  //   this.setState({
  //     playlists: retrievedPlaylists
  //   });
  // }

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
