import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

//TODO: add REST method to api for retrieving data with 1 call
const playlistData = [
  {
    id: 0,
    name: "TGIF",
    image: "default.jpg",
    playlistItems: [
      "melk",
      "bier",
      "wijn",
      "fruitsapje"
    ]
  },
  {
    id: 1,
    name: "Bier",
    image: "bier.jpg",
    playlistItems: [
      "Palm",
      "Tripel",
      "wijn",
      "fruitsapje"
    ]
  },
  {
    id: 2,
    name: "Van Wijn wordt je geen chagerijn",
    image: "wijn.jpg",
    playlistItems: [
      "Champagne",
      "Rode wijn",
      "Witte wijn"
    ]
  }
];

function renderHeader(){
  return (
    <header className="App-header">
      <img src={logo} className="App-logo" alt="logo" />
      <h1 className="App-title">The Beverage Randomizer</h1>
    </header>
  );
}


class App extends Component {



  render() {
    return (
      <div className="App">
        { renderHeader() }
        {/* <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header> */}
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
      </div>
    );
  }
}

export default App;
