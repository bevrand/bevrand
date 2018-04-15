import React, { Component } from 'react';
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
        value = {props.value}
      />
      <label htmlFor={props.id}></label>
    </div>
  );
};

class Register extends Component {
  constructor(props) {
    super(props);

    this.state = {
      submitName : "",
      submitEmail : "",
      submitPassword : "",
      controlPassword: "",
      message : "You are about to sign up",
      mounted: false
    }
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
  }

  componentDidMount() {
    this.setState({ mounted: true});
  }

  handleInputChange(event) {
    const target = event.target;
    const value =  target.value;
    const name = target.id;

    this.setState({
      [name]: value
    });
  }

  clearFields = () => {
    this.setState(
      {
        message: "Welcome " + this.state.submitName + " you are now ready to Randomize",
        submitName : "",
        submitEmail : "",
        submitPassword : "",
        controlPassword: "",
      }
    )
    console.log(this.state.submitName)
  }

  async handleSubmit(event) {
    event.preventDefault();
    if (this.state.submitName !== this.state.controlPassword)
    {
      this.state.message = "Passwords do not match";
      return;
    }
    let data = {
      username: this.state.submitName,
      emailAddress: this.state.submitEmail,
      passWord: this.state.submitPassword,
      active: true
    };
    let body;
    let status;
    try {
      let response = await fetch(`/api/register`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: new Headers({
          'Content-Type': 'application/json'
        })
      });
      body = await response.json();
      status = response.status;
    } catch (e) {
      console.log(e);
    }
    if (status !== 200)
    {
      console.log(body)
      var parts = body.message.split('-')[1].replace(/['"]+/g, '').replace(/[{}]/g, "");
      this.setState({
        message: parts,
      })
      return;
    }
    this.clearFields();  
}
  
  render() {
    return (

      <div className="Register">

      <form onSubmit={this.handleSubmit}>
      <h4>{this.state.message}</h4>
      <Input 
        id="submitName" 
        type="text"
        validator="true"
        minCharacters="4"
        value={this.state.submitName} 
        placeholder="Username" 
        onChange={this.handleInputChange} 
       />

       <Input 
         id="submitEmail" 
         type="email" 
         value={this.state.submitEmail}  
         placeholder="YourEmail@gmail.com" 
         onChange={this.handleInputChange}
       />

      <Input
        id="submitPassword" 
        type="password" 
        value={this.state.submitPassword} 
        placeholder="password" 
        onChange={this.handleInputChange}
       />

      <Input
        id="controlPassword" 
        type="password" 
        value={this.state.controlPassword} 
        placeholder="retype password" 
        onChange={this.handleInputChange}
       />

       <button type="submit">
        Register! 
        <i className="fa fa-fw fa-chevron-right"></i>
       </button>


        </form>
      </div>

    );
  }
}

export default Register;

