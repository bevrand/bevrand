import React, { Component } from 'react';
import './masthead.css';

class Masthead extends Component {
  render() {
    return (
      <header class="masthead">
        <div class="header-content">
          <div class="header-content-inner">
            <h1 id="homeHeading">The Beverage Randomizer</h1>
            {/* <hr> */}
            <p>All those Beverage choices bringing you down? Feeling lucky? Let fate quench your thirst with the Beverage Randomizer. Like you know, for randomizing your beverages.</p>
            <a class="btn btn-primary btn-xl js-scroll-trigger" href="#about">Let's get started!</a>
            <a class="btn btn-primary btn-xl js-scroll-trigger" href="#portfolio">Choose list</a>
            <a class="btn btn-primary btn-xl js-scroll-trigger" href="#services">How does it work?</a>
          </div>
        </div>
      </header>
    );
  }
}

export default Masthead;
