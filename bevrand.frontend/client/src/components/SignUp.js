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
      />
      <label htmlFor={props.id}></label>
    </div>
  );
};

class SignUp extends Component {
  constructor(props) {
    super(props);

    this.state = {
      submitName : "",
      submitEmail : "",
      submitPassword : "",
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

  async handleSubmit(event) {
    event.preventDefault();
    let data = {
      username: this.state.submitName,
      emailAddress: this.state.submitEmail,
      passWord: this.state.submitPassword,
      active: true
    };
  
    let body;
    try {
      let response = await fetch(`http://0.0.0.0:4570/api/User`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: new Headers({
          'Content-Type': 'application/json'
        })
      });
      body = await response.json();
    } catch (e) {
      console.log(e);
    }
  
    console.log(body);
  }

  render() {
    return (
      <div className="SignUp">
      <form onSubmit={this.handleSubmit} >
        <Input id="submitName" type="text" submitName={this.state.submitName} placeholder="Username" onChange={this.handleInputChange} />
        <Input id="submitEmail" type="text" submitEmail={this.state.submitEmail}  placeholder="YourEmail@gmail.com" onChange={this.handleInputChange}/>
        <Input id="submitPassword" type="text" submitPassword={this.state.submitPassword} placeholder="password" onChange={this.handleInputChange}/>
       <button>
        Sign Up! <i className="fa fa-fw fa-chevron-right"></i>
     </button>
      </form>
      </div>

    );
  }
}

export default SignUp;
