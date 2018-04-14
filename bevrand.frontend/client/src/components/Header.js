import React from 'react';
import { Link } from 'react-scroll';

const Header = (props) => {
  return (
    <header className="masthead">
      <div className="header-content">
        <div className="header-content-inner">
          <h1 id="homeHeading">The Beverage Randomizer</h1>
          <hr />
          <p>All those Beverage choices bringing you down? Feeling lucky? Let fate quench your thirst with the Beverage Randomizer.
            Like you know, for randomizing your beverages.</p>
          <Link id="letsGetStartedButton" className="btn btn-primary btn-xl" smooth={true} duration={350} to="getstarted" href="">Let's get started!</Link>
          <Link id="topChooseListButton" className="btn btn-primary btn-xl" smooth={true} duration={350} to="playlists" href="">Choose list</Link>
          <Link id="topFiveLinkButton" className="btn btn-primary btn-xl" smooth={true} duration={350} to="topFiveSwitch" href="">How much has been randomized?</Link>
        </div>
      </div>
    </header>
  )
}

export default Header;