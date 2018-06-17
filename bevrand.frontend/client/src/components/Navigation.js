import React, { Component } from 'react';
import { Link } from 'react-router-dom';

const debounce = (func, wait) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  }
}

class Navigation extends Component {
  constructor(props) {
    super(props)
    this.state = {
      scrollPositionY: 0
    };
  }

  componentDidMount() {
    return window.addEventListener('scroll', debounce(this.handleScroll, 16));
  }

  componentWillUnMount() {
    return window.removeEventListener('scroll', debounce(this.handleScroll, 16));
  }

  handleScroll = () => {
    const scrollPositionY = +window.scrollY;
    return this.setState({ scrollPositionY });
  }

  render() {
    // Add a navbar-shrink class when more then 100 pixels have geen scrolled
    const navbarShrink = this.state.scrollPositionY > 100;
    const navClasses = 'navbar navbar-expand-lg navbar-light fixed-top';

    return (
      <nav className={(navbarShrink ? navClasses + ' navbar-shrink' : navClasses)} id="mainNav">
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
              <Link className="nav-link" to='/create'>Create</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to='/login' onClick={this.props.handleLogout}>Logout</Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    )
  }

}

export default Navigation;