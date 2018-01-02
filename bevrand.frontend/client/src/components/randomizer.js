import React from 'react';

const PreviewItem = (props) => {
  let amountRandomized = props.amount ? props.amount : 0;
  return (
    <li className="list-group-item justify-content-between">
      {props.value}
      <span className="badge badge-default badge-pill pull-right">{amountRandomized}</span>
    </li>
  );
}

const PlaylistPreview = (props) => {
  const listOfBeverages = props.beverages;
  return (
    <div>
      <ul className="list-group">
        {listOfBeverages.map((beverage, index) => 
          <PreviewItem key={index} value={beverage} />
        )}
      </ul>
    </div>
  );
}


/**
 * Randomizer, needs 1 playlist as prop input
 * @param {*} props 
 */
const Randomizer = (props) => {
  //TODO: make the rendering based on the supplied data
  //TODO: split this component up in several smaller components

  return (
    <section className="bg-primary" id="getstarted">
      <div className="container">
        <div className="row">
          <div className="col-lg-8 mx-auto text-center">
            <h2 className="section-heading text-white">{props.playlist.name}</h2>
            <hr className="light" />
          </div>
        </div>
        <div id="random-output" className="row"></div>
        <div className="row">
          <div className="col-lg-8 mx-auto text-center">
            <a id="randomize-button" className="btn btn-primary btn-xl" href="#getstarted">Randomize!</a>
            <a className="btn btn-primary btn-xl js-scroll-trigger" href="#portfolio">Choose list</a>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-8 mx-auto">
            <PlaylistPreview {...props.playlist}/>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Randomizer;
