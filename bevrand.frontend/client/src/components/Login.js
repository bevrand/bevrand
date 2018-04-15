import React, { Component } from 'react';
import './Login.css';
import AuthService from './AuthService';
import { CSSTransitionGroup } from 'react-transition-group';

const Input = (props) => {
  return (
    <div className="Input">
      <input 
        id={props.id}
        autoComplete="false" 
        required 
        type={props.type}
        placeholder={props.placeholder}
        onChange={props.onChange}
      />
      <label htmlFor={props.id}></label>
    </div>
  );
};

const Modal = (props) => {
  return (
    <div className="Modal">
      <form onSubmit={props.onSubmit} onChange={props.onChange} className={"ModalForm"}>
        <Input id="username" type="text" placeholder="Your UserName"/>
        <Input id="email" type="email" placeholder="YourEmail@gmail.com"/>
        <Input id="passWord" type="password" placeholder="password"/>
        <button>
          Log in <i className="fa fa-fw fa-chevron-right"></i>
        </button>
      </form>
      
    </div>
  );
}

class Login extends Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

    // Making AuthService available in this component
    this.Auth = new AuthService();

    this.state = {
      mounted: false
    }
  }

  componentWillMount() {
    if(this.Auth.loggedIn()) {
      console.log('Already logged in');
      //Redirect here to userpage
      //TODO: redirect to the user specific page
      this.props.history(`/user`);
    }
  }

  componentDidMount() {
    this.setState({ mounted: true});
  }

  handleSubmit(e) {
    console.log('Tried to login')
    e.preventDefault();

    this.Auth.login(this.state.username, this.state.email, this.state.passWord)
      .then(res => {
        // Redirect here to the a subset of the frontpage (with user data)
        this.props.history.replace(`/user/${this.state.username}`);
      })
      .catch(err => {
        alert(err);
      })
  }

  handleChange(e) {
    this.setState(
      {
        [e.target.id]: e.target.value
      }
    )
  }

  render() {
    let child;

    if(this.state.mounted) {
      child = (<Modal onSubmit={this.handleSubmit} onChange={this.handleChange} />)
    }

    return (
      <div className="Login">
				<CSSTransitionGroup 
					transitionName="login"
					transitionEnterTimeout={500}
					transitionLeaveTimeout={300}>
						{child}
				</CSSTransitionGroup>
			</div>
    );
  }

}


export default Login;
