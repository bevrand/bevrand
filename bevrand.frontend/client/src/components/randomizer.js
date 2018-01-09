import React, { Component } from 'react';
import axios from 'axios';

const PreviewItemRow = (props) => {
  const beverage = props.value;
  return (
    <li className="list-group-item text-center justify-content-between">
      {beverage}
      {/* <span className="badge badge-default badge-pill pull-right">0</span> */}
    </li>
  );
}

const PlaylistPreview = (props) => {
  const listOfBeverages = props.beverages;
  return (
    <div>
      <ul className="list-group">
        {listOfBeverages.map((beverage, index) =>
          <PreviewItemRow key={index} value={beverage} />
        )}
      </ul>
    </div>
  );
}

const RandomizeButton = (props) => {
  return (
    <div className="col-lg-8 mx-auto text-center">
      <a id="randomize-button" className="btn btn-primary btn-xl" onClick={props.onClick} href="#getstarted">Randomize!</a>
      <a className="btn btn-primary btn-xl js-scroll-trigger" href="#portfolio">Choose list</a>
    </div>
  )
}

const getRandomize = (playlist) => {
  let name = playlist.name;
  let playlistItems = playlist.beverages;
  axios.post(`http://randomizeapi:4560/api/randomize?user=frontpage&list=${name}`, {
    ...playlistItems
  })
    .then(response => {
      return response.data;
    })
    .catch(error => {
      console.error(error);
      return null;
    })
}


/**
 * Uses the provided Playlist to randomize a beverage
 * @param {object} playlist 
 */
const randomizeBeverageMock = (playlist) => {
  const amountOfBeverages = playlist.beverages.length;
  const randomizedIndex = Math.floor(Math.random() * (amountOfBeverages));
  return playlist.beverages[randomizedIndex];
}

/**
 * Randomizer, needs 1 playlist as prop input
 * @param {*} props 
 */
class Randomizer extends Component {
  constructor(props) {
    super(props);

    this.state = {
      result: null,
      playlist: this.props.playlist
    }

    this.handleRandomize = this.handleRandomize.bind(this);
  }

  componentWillReceiveProps(nextProps){
    this.setState({
      playlist: this.props.playlist
    });
  }

  handleRandomize(){
    //TODO:Update history of Randomized Beverages
    

    //Randomize the beverage
    // const randomizedBeverage = randomizeBeverageMock(this.props.playlist);
    const randomizedBeverage = getRandomize(this.props.playlist);
    
    //Set Result, so Component will be updated
    this.setState({
      result: randomizedBeverage
    });
  }

  //TODO: split this component up in several smaller components
  render() {
    const playlist = this.props.playlist;

    return (
      <section className="bg-primary" id="getstarted">
        <div className="container">
          <div className="row">
            <div className="col-lg-8 mx-auto text-center">
              <h2 className="section-heading text-white">{playlist.name}</h2>
              <hr className="light" />
            </div>
          </div>
          <div className="row">
            <RandomizeButton onClick={this.handleRandomize} />
          </div>
          <div id="random-output" className="row">
          {this.state.result != null &&
              <div className="alert alert-success" role="alert">
                You have randomized: {this.state.result}
              </div>
            }
          </div>
          <div className="row">
            <div className="col-lg-8 mx-auto">
              <PlaylistPreview {...playlist} />
            </div>
          </div>
        </div>
      </section>
    );
  }
}


export default Randomizer;
