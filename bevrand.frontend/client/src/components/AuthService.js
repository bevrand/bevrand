import decode from 'jwt-decode';

export default class AuthService {
  constructor() {
    this.fetch = this.fetch.bind(this);
    this.login = this.login.bind(this);
    this.getProfile = this.getProfile.bind(this);
  }

  //TODO: add signup / register to authservice, to make it 1 central class
  //TODO: add encryption to this class
  register(userName, emailAddress, passWord) {
    return this.fetch('api/register', {
      method: 'POST',
      body: JSON.stringify({
        userName,
        emailAddress,
        passWord
      })
    })
  }
  
  login(userName, emailAddress, passWord) {
    return this.fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify({
        userName,
        emailAddress,
        passWord
      })
    }).then(res => {
      this.setToken(res.token)
      return Promise.resolve(res);
    })
  }

  loggedIn() {
    const token = this.getToken();
    return !!token && !this.isTokenExpired(token);
  }

  isTokenExpired(token) {
    try {
      const decoded = decode(token);
      if(decoded.exp < Date.now() / 1000) {
        return true;
      } else {
        return false;
      }
    } catch (err) {
      return false;
    }
  }

  setToken(idToken) {
    localStorage.setItem('id_token', idToken);
  }

  getToken() {
    return localStorage.getItem('id_token');
  }

  logout() {
    localStorage.removeItem('id_token');
  }

  getProfile() {
    return decode(this.getToken());
  }

  fetch(url, options) {
    const headers = {
      'Accept': 'application/json',
      'Content-type': 'application/json'
    }

    if(this.loggedIn()) {
      console.log('Logged in? ', this.loggedIn());
      headers['Authorization'] = 'Bearer' + this.getToken()
    }

    return fetch(url, {
      headers,
      ...options
    })
      .then(this._checkStatus)
      .then(response => response.json())
  }

  async _checkStatus(response) {
    if(response.status >= 200 && response.status < 300) {
      return response;
    } else if(response.status === 400) {
      // If response is an 400 then username / emailAddress already exists
      let parsedResponse = await response.json();
      let error = new Error(parsedResponse.message.split('-')[1].replace(/['"]+/g, '').replace(/[{}]/g, ""))
      throw error;
    } else {
      let error = new Error(response.statusText);
      error.response = response;
      throw error;
    }
  }
}