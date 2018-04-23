import React, { Component } from 'react';
import { CSSTransitionGroup } from 'react-transition-group';

import AuthService from './AuthService';
import './Login.css';

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
        <h4>{props.message}</h4>
        {/* minCharacters="4" validator="true" */}
        <Input id="userName" type="text" placeholder="Your UserName"/>
        <Input id="emailAddress" type="email" placeholder="YourEmail@gmail.com"/>
        <Input id="passWord" type="password" placeholder="password"/>
        <Input id="controlPassWord" type="password" placeholder="Retype password"/>
        <button type="submit">
          Register! <i className="fa fa-fw fa-chevron-right"></i>
        </button>
      </form>
      
    </div>
  );
}

class Register extends Component {
  constructor(props) {
    super(props);

    this.Auth = new AuthService();

    this.state = {
      message : "You are about to register",
      mounted: false
    }
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
  }

  componentDidMount() {
    this.setState({ mounted: true});
  }

  handleInputChange(e) {
    this.setState({
        [e.target.id]: e.target.value
    })
  }

  clearFields = (userName) => {
    this.setState(
      {
        message: "Welcome " + userName + " you are now ready to Randomize",
        userName : "",
        emailAddress : "",
        passWord : "",
        controlPassWord: "",
      }
    )
    console.log(userName)
  }

  handleSubmit(e) {
    e.preventDefault();
    if (this.state.passWord !== this.state.controlPassWord)
    {
      console.log('Passwords do not match')
      this.setState({
        message: "Passwords do not match",
      })
      return;
    }

    this.Auth.register(this.state.userName, this.state.emailAddress, this.state.passWord)
      .then(res => {
        console.log(`Succesful register of ${res.username}`);
        this.clearFields(this.state.userName);
        this.props.history.replace('/login');
      })
      .catch(err => {
        this.setState({
          message: `Oops, something went wrong: ${err.message}`
        })
      })
}
  
  render() {
    let child;

    if(this.state.mounted) {
      child = (
        <Modal 
          message={this.state.message} 
          onSubmit={this.handleSubmit} 
          onChange={this.handleInputChange} 
        />)
    }

    return (
      <div className="Register">
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

export default Register;

