import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = (props) => {
  return (
    <nav class="navbar navbar-expand-lg navbar-light fixed-top" id="mainNav">
      <div class="container">
        {/* <a class="navbar-brand js-scroll-trigger" href="#page-top">The Beverage Randomizer</a> */}
        <Link className='navbar-brand' to='/'>The Beverage Randomizer</Link>
        <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive"
          aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              {/* <a class="nav-link js-scroll-trigger" href="#services">How</a> */}
              <Link to='/login'></Link>
            </li>
            <li class="nav-item">
              <Link to='/register'>
              {/* <a class="nav-link js-scroll-trigger" href="#getstarted">Get Started</a> */}
            </li>
            {/* <li class="nav-item">
              {/* <a class="nav-link js-scroll-trigger" href="#portfolio">Playlists</a> */}
            </li>
            <li class="nav-item">
              {/* <a class="nav-link js-scroll-trigger" href="#contact">Contact</a> */}
            </li> */}
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navigation;