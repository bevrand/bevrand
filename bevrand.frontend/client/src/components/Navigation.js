import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = (props) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light fixed-top" id="mainNav">
      <div className="container">
        {/* <a className="navbar-brand js-scroll-trigger" href="#page-top">The Beverage Randomizer</a> */}
        <Link className='navbar-brand' to='/'>The Beverage Randomizer</Link>
        <button className="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive"
          aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarResponsive">
          <ul className="navbar-nav ml-auto">
            <li className="nav-item">
              {/* <a className="nav-link js-scroll-trigger" href="#services">How</a> */}
              <Link className="nav-link" to='/login'></Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to='/register'></Link>
              {/* <a className="nav-link js-scroll-trigger" href="#getstarted">Get Started</a> */}
            </li>
            <li className="nav-item">
              {/* <a className="nav-link js-scroll-trigger" href="#portfolio">Playlists</a> */}
            </li>
            <li className="nav-item">
              {/* <a className="nav-link js-scroll-trigger" href="#contact">Contact</a> */}
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navigation;