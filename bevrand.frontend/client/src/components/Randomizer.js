import React, { Component } from 'react';

const PreviewItemRow = (props) => {
  return (
    <li className="list-group-item text-center justify-content-between">
      {props.name.toString()}
      <span className="badge badge-default badge-pill pull-right">{props.rolled.toString()}</span>
    </li>
  );
}

const PlaylistPreview = (props) => {
  const listOfBeverages = props.beverages;
  return (
    <div>
      <ul className="list-group">
        {listOfBeverages.map((beverage, index) =>
          <PreviewItemRow key={index} name={beverage.drink} rolled={beverage.rolled} />
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
  let data = {
    user: "frontpage",
    list: `${playlist.name}`,
    beverages: playlist.beverages
  };

  let body;
  try {
    let response = await fetch(`/api/randomize?user=frontpage&list=${playlist.name}`, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    });
    body = await response.json();
  } catch (e) {
    console.log(e);
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
      let resultBody = await getRandomize(this.props.playlist);
      this.props.updateBeverages(resultBody.history)
      this.setState({
        result: resultBody.result
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
              <h2 className="section-heading text-white">{playlist.name}</h2>
              <hr className="light" />
            </div>
          </div>
          <div className="row">
            <RandomizeButton onClick={this.handleRandomize} />
          </div>
          <div id="random-output" className="row">
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
