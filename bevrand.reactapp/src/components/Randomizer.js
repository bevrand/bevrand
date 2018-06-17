import React, { Component } from 'react';
import { Link } from 'react-scroll';

import config from './ConfigService'

const PreviewItemRow = (props) => {
  return (
    <li id={`currentlySelectedBeverages${props.rowId}`} className="list-group-item text-center justify-content-between">
      {props.name.toString()}
    </li>
  );
}

const PlaylistPreview = (props) => {
  const listOfBeverages = props.beverages;
  return (
    <div>
      <ul className="list-group">
        {listOfBeverages.map((beverage, index) =>
          <PreviewItemRow key={index} rowId={index} name={beverage} />
        )}
      </ul>
    </div>
  );
}

const RandomizeButton = (props) => {
  return (
    <div className="col-lg-8 mx-auto text-center">
      <a id="randomizeButton" className="btn btn-primary btn-xl text-white" onClick={props.onClick}>Randomize!</a>
      <Link id="chooseListBottomButton" className="btn btn-primary btn-xl text-white" smooth={true} duration={350} href="" to="playlists">Choose a list</Link>
    </div>
  )
};

const getRandomize = async (playlist, username) => {
  let body;
  try {
    //TODO: Create generic service for Proxy calls (like AuthService)
    let response = await fetch(`${config.proxyHostname}/api/randomize`, {
      method: 'POST',
      body: JSON.stringify({
        user: username || "frontpage",
        list: `${playlist.list}`,
        beverages: playlist.beverages
      }),
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    });
    body = await response.text();
  } catch (err) {
    console.error(err);
  }

  return body;
};

/**
 * Randomizer, needs 1 playlist as prop input
 * @param {*} props 
 */
class Randomizer extends Component {
  constructor(props) {
    super(props);

    this.state = {
      result: null
    }

    this.handleRandomize = this.handleRandomize.bind(this);
  }

  async handleRandomize() {
    //Randomize the beverage
    try {
      let resultBody = await getRandomize(this.props.playlist, this.props.userName);
      this.setState({
        result: resultBody
      });
    } catch (error) { console.log(error); }
  }

  //TODO: split this component up in several smaller components
  render() {
    let playlist = this.props.playlist;

    return (
      <section className="bg-primary" id="getstarted">
        <div className="container">
          <div className="row">
            <div className="col-lg-8 mx-auto text-center">
              <h2 id="currentlySelectedPlaylist" className="section-heading text-white">{playlist.displayName}</h2>
              <hr className="light" />
            </div>
          </div>
          <div className="row">
            <RandomizeButton onClick={this.handleRandomize} />
          </div>
          <div id="randomizedOutput" className="row">
            {/* TODO: add animation to this section */}
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
