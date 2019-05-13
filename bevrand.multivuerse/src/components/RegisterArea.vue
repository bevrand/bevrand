<template>
  <div class="registerarea">
    <h2>Your adventure starts here!</h2>
    <form id="registerForm" @submit="checkForm">
      <section class="inputarea">
          <input
            type="text"
            class="inputfield"
            placeholder="Username"
            v-model="username"
            id="username"
          />
        <br />
        <input
           type="email"
           v-model="email"
           placeholder="Email"
           id="email"
           class="inputfield"/>
        <br />
          <input
            type="password"
            id="password"
            placeholder="Password"
            class="inputfield"
            v-model="password"
            autocomplete="off"
          />
        <br />
          <input
            type="password"
            id="repeat-password"
            class="inputfield"
            placeholder="Repeat Password"
            v-model="confirmPassword"
            autocomplete="off"
          />
        <br />
        <button
                id="signUpButton"
                class="signupbutton"
                >Sign Up</button>
      </section>
    </form>
  </div>
</template>

<script>

export default {
  name: "Register",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      registerResponse: ""
    };
  },
  components: {
  },
  computed: {
  },
  methods: {
    checkForm: function(e) {
      let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      if (!this.username) {
        this.alert("Username is required");
      } else if (this.username.length < 4 || this.username.length > 21) {
        this.alert("Username should be between 3 and 20 characters");
      } else if (!this.email) {
        this.alert("Email is required");
      } else if(!re.test(this.email)) {
        this.alert(`${this.email} is not a valid emailaddres`);
      } else if (this.password.length < 4 || this.password.length > 29) {
        this.alert("Password should be between 3 and 28 characters");
      } else if (this.password !== this.confirmPassword) {
        this.alert("Passwords do not match");
      } else {
        this.signUp();
      }

      e.preventDefault();
    },

    signUp: function() {
      this.$apiClient({
        method: "post",
        url: `${this.$proxyUrl}/authentication-api/register`,
        data: {
            "username": this.username,
            "emailAddress": this.email,
            "password": this.password
        }
      })
        .then(response => {
            this.$apiClient({
              method: 'post',
              url: `${this.$proxyUrl}/authentication-api/login`,
              data: {
                "emailAddress" : this.email,
                "password": this.password,
                "username": this.username
              }
            }).then(response => {
              this.token = response.data['token'];
              this.$store.commit('setToken', response.data);
              this.$router.push({ name: 'reroutePage', params: { username: this.username } });
            })
        })
        .catch(e => {
          let errorText = 'Something went wrong';
          this.registerResponse = e.response.data;
          if (e.response.status === 400) {
              let splitError = JSON.parse(e.response.data['message'].substring(e.response.data['message'].indexOf('-') +1));
              let alreadyExists = splitError['Error'].includes("already exists");
              if (alreadyExists) {
                  if (splitError['Error'].includes("User"))
                      errorText = "Username already exists please try another";
                  else{
                      errorText = "Email already exists please try another";
                  }
              }
          }
        if (e.response.status === 500 || e.response.status === 503) {
            errorText = "Servers are down please try again later";
        }
            this.alert(errorText);
        });
    },
    alert: function(text) {
      this.$swal("Something went wrong", text, "error")
    }
  }
};
</script>

<style scoped>
.inputarea {
  margin-top: 2em;
  margin-left: 22em;
  margin-right: 22em;
  text-align: center;
}

@media screen and (max-width: 1366px) {
  .inputarea {
    margin-top: 2em;
    margin-left: 10em;
    margin-right: 10em;
    text-align: center;
  }
}

@media screen and (max-width: 650px) {
  .inputarea {
    margin-top: 2em;
    margin-left: 1em;
    margin-right: 1em;
    text-align: center;
  }
}

h2 {
  font-weight: bold;
  margin-top: 1em;
  font-size: 2em;
  text-align: center;
}

#signUpButton {
  position: relative;
  display: inline-block;
  background: #ff9500;
  color: #ffffff;
  text-align: center;
  border-radius: 0.5em;
  text-decoration: none;
  padding: 0.65em 3em 0.65em 3em;
  margin-top: 2em;
  margin-bottom: 2em;
  cursor: pointer;
  outline: 0;
  font-weight: 400;
  font-size: 1em;
  font-family: "Ubuntu", sans-serif;
  -moz-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
    border-bottom-color 0.35s ease-in-out;
  -webkit-transition: background-color 0.35s ease-in-out,
    color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
  -ms-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
    border-bottom-color 0.35s ease-in-out;
  transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
    border-bottom-color 0.35s ease-in-out;
}

#signUpButton:hover {
  color: #fff;
  background: #424242;
  letter-spacing: 1px;
  -webkit-box-shadow: 0px 5px 40px -10px rgba(0, 0, 0, 0.57);
  -moz-box-shadow: 0px 5px 40px -10px rgba(0, 0, 0, 0.57);
  box-shadow: 5px 40px -10px rgba(0, 0, 0, 0.57);
  transition: all 0.4s ease 0s;
}

.inputfield {
  font-family: "Ubuntu", sans-serif;
  margin: auto;
  display: block;
  padding: 5px;
  border: none;
  font-size: 16px;
  width: 75%;
  color: #424242;
  background-color: white;
}

</style>