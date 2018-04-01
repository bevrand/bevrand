import React, { Component } from 'react';
import './Login.css';
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
      />
      <label htmlFor={props.id}></label>
    </div>
  );
};

const Modal = (props) => {
  return (
    <div className="Modal">
      <form onSubmit={props.onSubmit} className={"ModalForm"}>
        <Input id="name" type="text" placeholder="Your Name"/>
        <Input id="username" type="email" placeholder="YourEmail@gmail.com"/>
        <Input id="password" type="password" placeholder="password"/>
      </form>
      <button>
        Log in <i className="fa fa-fw fa-chevron-right"></i>
      </button>
    </div>
  );
}

class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      mounted: false
    }
  }

  componentDidMount() {
    this.setState({ mounted: true});
  }

  handleSubmit(e) {
    console.log('Tried to login')
    // e.preventDefault();
  }

  render() {
    let child;

    if(this.state.mounted) {
      child = (<Modal onSubmit={this.handleSubmit} />)
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
