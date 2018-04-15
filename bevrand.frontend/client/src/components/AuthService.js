import decode from 'jwt-decode';

export default class AuthService {
  constructor() {
    this.fetch = this.fetch.bind(this);
    this.login = this.login.bind(this);
    this.getProfile = this.getProfile.bind(this);
  }

  //TODO: add signup / register to authservice, to make it 1 central class
  
  login(username, email, passWord) {
    return this.fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify({
        username,
        email,
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
      headers['Authorization'] = 'Bearer' + this.getToken()
    }

    return fetch(url, {
      headers,
      ...options
    })
      .then(this._checkStatus)
      .then(response => response.json())
  }

  _checkStatus(response) {
    if(response.status >= 200 && response.status < 300) {
      return response;
    } else {
      let error = new Error(response.statusText);
      error.response = response;
      throw error;
    }
  }
}