import React, { Component } from 'react';
import { CSSTransitionGroup } from 'react-transition-group';
import uuidv5 from 'uuid/v5'

import AuthService from './AuthService';
import config from './ConfigService';

const PlaylistForm = (props) => {
  const greeterText = `Create a custom Playlist here: ${props.user}`;
  return (
    <section className="bg-primary" id="playlistCreator">
      <div className="container">
        <div className="row">
          <div className="col-lg-8 mx-auto text-center">
            <form onSubmit={props.onSubmit} onChange={props.onChange} className={"PlaylistForm"}>
              <h2 id="currentlySelectedPlaylist" className="section-heading text-white">{greeterText}</h2>
              <div className="Input">
                <input 
                  id="displayName"
                  autoComplete="false" 
                  required 
                  type="text"
                  placeholder="Name of your playlist"
                  onChange={props.onChange}
                />
                <label htmlFor="displayName"></label>
              </div>
              <div className="Input">
                <input 
                  id="beverages"
                  autoComplete="false" 
                  required 
                  type="text"
                  placeholder="Beverages, seperate entries with commas"
                  onChange={props.onChange}
                />
                <label htmlFor="beverages"></label>
              </div>
              <hr className="light" />
              <button type="submit">
                Create the Playlist! <i className="fa fa-fw fa-chevron-right"></i>
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}

class PlaylistCreator extends Component {
  constructor(props) {
    super(props);
    
    this.Auth = new AuthService();

    this.state = {
      mounted: false
    }

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    this.setState({
      mounted: true
    })
  }

  handleInputChange(e) {
    this.setState({
      [e.target.id]: e.target.value
    });
  }

  handleSubmit(e) {
    e.preventDefault();

    const beverages = this.state.beverages.split(',')
    const MY_NAMESPACE= 'b3d85439-b4b8-43d6-bdde-9d109e3ccb90';


    //TODO: Create generic service for api calls (like AuthService)
    this.Auth.fetch(`${config.proxyHostname}/api/user`, {
      method: 'POST',
      body: JSON.stringify({
        beverages: beverages,
        displayName: this.state.displayName,
        imageUrl: 'https://static.beveragerandomizer.com/file/beveragerandomizer/images/users/standardimage.png',
        list: uuidv5(this.state.displayName, MY_NAMESPACE),
        user: this.Auth.getProfile().username
      })
    })

    this.props.history.replace('/user');
  }

  render() {
    let child;
    let user = this.Auth.getProfile().username;

    if(this.state.mounted) {
      child = (
        <PlaylistForm 
          user={user}
          onChange={this.handleInputChange}
          onSubmit={this.handleSubmit}
        />
        
      )
    }

    return (
      <div className="PlaylistCreator">
        <CSSTransitionGroup 
					transitionName="login"
					transitionEnterTimeout={500}
					transitionLeaveTimeout={300}>
						{child}
				</CSSTransitionGroup>
      </div>
    )
  }
}

export default PlaylistCreator;