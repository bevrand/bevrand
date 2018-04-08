import React from 'react';

const Navigation = (props) => {
  return (
    <header class="masthead">
      <div class="header-content">
        <div class="header-content-inner">
          <h1 id="homeHeading">The Beverage Randomizer</h1>
          <hr />
          <p>All those Beverage choices bringing you down? Feeling lucky? Let fate quench your thirst with the Beverage Randomizer.
            Like you know, for randomizing your beverages.</p>
          <a id="letsGetStartedButton" class="btn btn-primary btn-xl js-scroll-trigger" href="#getstarted">Let's get started!</a>
          <a id="topChooseListButton" class="btn btn-primary btn-xl js-scroll-trigger" href="#portfolio">Choose list</a>
          <a id="howDoesItWorkButton" class="btn btn-primary btn-xl js-scroll-trigger" href="#services">How does it work?</a>
        </div>
      </div>
    </header>
  )
}