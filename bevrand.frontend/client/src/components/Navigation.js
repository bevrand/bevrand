import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = (props) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light fixed-top" id="mainNav">
      <div className="container">
        <Link className='navbar-brand' to='/'>The Beverage Randomizer</Link>
        <button className="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive"
          aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarResponsive">
          <ul className="navbar-nav ml-auto">
            <li className="nav-item">
              <Link className="nav-link" to='/login'>Login</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to='/register'>Register</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to='/user'>User</Link>
            </li>
            <li className="nav-item">
            {/* TODO: decide if href is needed here */}
              <a className="nav-link" href="" onClick={props.handleLogout}>Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navigation;