<template>
  <div class="registerarea">
    <h2>Your adventure starts here!</h2>
    <form id="registerForm" @submit="checkForm">
      <section class="inputarea">
        <FloatingLabel
          :config="{
            label: 'Username',
            name: 'username',
            line: false,
            color: {
              focusColor: '#00FA9A',
              errorColor: '#ff0000',
              lineColor: '#00FA9A',
              blurredColor: 'rgba(3, 23, 40, 0.34)'
            },
            hasError: usernameValidation,
            hasClearButton: false
          }"
        >
          <input
            type="text"
            class="inputfield"
            v-model="username"
            id="username"
          />
        </FloatingLabel>
        <br />
        <FloatingLabel
          :config="{
            label: 'Email',
            name: 'email',
            line: false,
            color: {
              focusColor: '#00FA9A',
              errorColor: '#ff0000',
              lineColor: '#00FA9A',
              blurredColor: 'rgba(3, 23, 40, 0.34)'
            },
            hasError: !emailValidation,
            hasClearButton: false
          }"
        >
        <input type="email"
               v-model="email"
               id="email"
               class="inputfield"/>
        </FloatingLabel>
        <br />
        <FloatingLabel
          :config="{
            label: 'Password',
            name: 'password',
            line: false,
            color: {
              focusColor: '#00FA9A',
              errorColor: '#ff0000',
              lineColor: '#00FA9A',
              blurredColor: 'rgba(3, 23, 40, 0.34)'
            },
            hasError: hasError,
            hasClearButton: false
          }"
        >
          <input
            type="password"
            id="password"
            class="inputfield"
            v-model="password"
            autocomplete="off"
          />
        </FloatingLabel>
        <br />
        <FloatingLabel
          :config="{
            label: 'Retype Password',
            name: 'confirmPassword',
            color: {
              focusColor: '#00FA9A',
              errorColor: '#ff0000',
              lineColor: '#00FA9A',
              blurredColor: 'rgba(3, 23, 40, 0.34)'
            },
            line: false,
            hasError: hasError,
            hasClearButton: false
          }"
        >
          <input
            type="password"
            id="repeat-password"
            class="inputfield"
            v-model="confirmPassword"
            autocomplete="off"
          />
        </FloatingLabel>
        <small v-if="hasError" style="color: #f00; font-weight: bold"
          >Passwords do not match</small
        >
        <br />
        <button id="signUpButton" class="signupbutton">Sign Up</button>
      </section>
    </form>
  </div>
</template>

<script>
import FloatingLabel from "vue-simple-floating-labels";

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
    FloatingLabel
  },
  computed: {
    hasError() {
      return this.password !== this.confirmPassword;
    },
    emailValidation() {
      let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(this.email);
    },
    usernameValidation() {
      return this.username.length < 4 || this.username.length > 21;
    }
  },
  methods: {
    checkForm: function(e) {
      if (!this.username) {
        this.alert("Username is required");
      } else if (this.username.length < 4 || this.username.length > 21) {
        this.alert("Username should be between 3 and 20 characters");
      } else if (!this.email) {
        this.alert("Email is required");
      } else if (this.password.length < 4 || this.password.length > 29) {
        this.alert("Password must be between 3 and 28 characters");
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
        url: "http://0.0.0.0:4540/api/register",
        //this should become username and password after refactor
        data: {
            "userName": this.username,
            "emailAddress": this.email,
            "passWord": this.password
        }
      })
        .then(response => {
            this.$router.push({ name: 'reroutePage', params: { username: this.username } });
          this.alert(response.data + "done!");
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
      this.$alertify.alertWithTitle(text, () =>
        this.$alertify.warning("alert is closed")
      );
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
  width: 8em;
  background-color: white !important;
}
</style>