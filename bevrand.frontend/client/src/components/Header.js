import React from 'react';
import { Link } from 'react-scroll';

const Header = (props) => {
  return (
    <header className="masthead">
      <div className="header-content">
        <div className="header-content-inner">
          <h1 id="homeHeading">The Beverage Randomizer</h1>
          <hr />
          <p>{ props.headerText }</p>
          <Link id="letsGetStartedButton" className="btn btn-primary btn-xl" smooth={true} duration={350} to="getstarted" href="">Let's get started!</Link>
        </div>
      </div>
    </header>
  )
}

export default Header;