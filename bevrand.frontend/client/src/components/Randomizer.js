import React, { Component } from 'react';

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
};

const getRandomize = async (playlist) => {
  let url = `/api/randomize?user=frontpage&list=${playlist.name}`;
  let data = {
    user: "frontpage",
    list: `${playlist.name}`,
    beverages: playlist.beverages
  };

  const response = await fetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: new Headers({
      'Content-Type': 'application/json'
    })
  })
  const body = await response.json();

  if(response.status !== 200) throw Error(body.message);

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

  handleRandomize(){
    //TODO:Retrieve new Redis randomize information for the active playlist

    //Randomize the beverage
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
