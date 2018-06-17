import React, { Component } from 'react';

import config from './ConfigService'

const getRedisHistory = async (playlist, toggle) => {
  let body;
  try {
    const response = await fetch(`${config.proxyHostname}/api/redis?user=${playlist.user.toLowerCase()}&list=${playlist.list}&topfive=${toggle}`, {
        method: 'GET'
      });
    body = await response.json();
  } catch (err) {
    console.error('Error: ', err);
  }
  return body;
}

const RenderAnItemRow = (props) => {
  let drink = props.item.drink
  let rolled = props.item.rolled
  return (
    <li id={`highestRolledDrinks${props.rowId}`} className="list-group-item text-center justify-content-between">
      {`${drink.toString()}`} {`has been rolled : ${rolled.toString()} times`}
    </li>
  );
}

/**
 * TopRolledBeverages, needs 1 playlist as prop input
 * @param {*} props 
 */
class TopRolledBeverages extends Component {
  constructor(props) {
    super(props);
    this.state = {
      result: null,
      toggle : false      
    }
  }

  componentDidMount() {
    this.handleRedisHistory()
    this.timerID = setInterval(
      () => this.handleRedisHistory(),
      60000
    );
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }
  
  async handleRedisHistory() {
    //Get the history from redis
    try {
      let resultBody = await getRedisHistory(this.props.playlist, this.state.toggle);
      this.setState({
        result : resultBody
      });
    } catch (error) { console.log(error); }
  }

  handleToggleForTopFive = () => {
     this.setState((prevState, props) => ({
      toggle: !prevState.toggle
    }), () => {this.handleRedisHistory()});
  }

  render() {
    let playlist = this.props.playlist;
    let arrayListName = `${playlist.user.toString().toLowerCase()}:${playlist.list.toString().toLowerCase()}`
    let textValue;
    if(this.state.toggle) {
        textValue = "The Top Five"
    }
    else {
      textValue = "All drinks in this list"
    }

    let someArray;
    if(this.state.result != null) {
      someArray = this.state.result[arrayListName]
    }
    return (
      <section className="bg-primary" id="topFiveSwitch">
        <div className="container">
          <div className="row">
            <div className="col-lg-8 mx-auto text-center">
              <h2 id="currentlySelectedPlaylist" className="section-heading text-white">{playlist.displayName}</h2>
              <h4 id="currentlySelectedPlaylist" className="section-heading text-white">For this list the following drinks were randomized</h4>
              <hr className="light" />
            </div>
          </div>
          <div className="row">
            <div className="col-lg-8 mx-auto text-center">
            <a id="topFiveSwitchButton" className="btn btn-primary btn-xl text-white" onClick={this.handleToggleForTopFive}>{textValue}</a>
            </div>
          </div>
          <div id="redisHistoryForList" className="row">
            <div className="col-lg-8 mx-auto">
          <ul className="list-group">
          {someArray != null && someArray.map((someElement, index) => <RenderAnItemRow key={index} rowId={index} item={someElement}/>)}
          </ul>
          </div>
        </div>
        </div>
      </section>
    );
  }
}

export default TopRolledBeverages;