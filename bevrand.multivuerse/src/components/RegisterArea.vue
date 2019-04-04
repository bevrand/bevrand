<template>
    <div class="registerarea">
        <h2>Your adventure starts here!</h2>
        <form id="registerForm" @submit="checkForm">
            <section class="inputarea">
                <input type="text"
                       placeholder="Username"
                       class="inputfield"
                       v-model="username"
                       id="username">
                <br>
                <input type="email"
                       placeholder="Email"
                       v-model="email"
                       class="inputfield"
                       id="email">
                <br>
                <input type="password"
                       id="password"
                       placeholder="Password"
                       v-model="password"
                       class="inputfield"
                       autocomplete="off">
                <br>
                <input type="password"
                       id="repeat-password"
                       placeholder="Repeat your password"
                       v-model="confirmPassword"
                       class="inputfield"
                       autocomplete="off">
                <button
                        id="signUpButton"
                        class="signupbutton">Sign Up
                </button>
            </section>
        </form>
    </div>
</template>

<script>
    export default {
        name: "Register",
        data() {
            return {
                username: '',
                email: '',
                password: '',
                confirmPassword: '',
            }
        },

        methods: {
            checkForm: function (e) {
                if (!this.username) {
                    this.alert("Username is required")
                }
                else if (this.username.length < 4 || this.username.length > 21) {
                    this.alert("Username should be between 3 and 20 characters")
                }
                else if (!this.email) {
                    this.alert("Email is required")
                }
                else if (this.password.length < 4 || this.password.length > 21) {
                    this.alert("Password must be between 3 and 20 characters")
                }
                else if (this.password !== this.confirmPassword ) {
                    this.alert("Passwords do not match")
                }
                else {
                    this.signUp();
                }

                e.preventDefault();
            },

            signUp: function () {
                this.$apiClient({
                    method: 'post',
                    url: 'http://0.0.0.0:4540/api/register',
                    data: {
                        "username" : this.username,
                        "emailAddress" : this.emailAddress,
                        "password": this.password,
                    }
                    })
                    .then((response) => {
                        this.alert(response.data + "done!");
                    })
                    .catch(e => {
                        this.alert(e)
                    })
            },
            alert: function(text){
                this.$alertify.alertWithTitle(text, () =>
                    this.$alertify.warning("alert is closed"))
            },
        }
    }
</script>

<style scoped>

    .inputarea {
        margin-top: 2em;
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
        background: #FF9500;
        color: #FFFFFF;
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
        font-family: 'Ubuntu', sans-serif;
        -moz-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
        -webkit-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
        -ms-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
        transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
    }

    #signUpButton:hover {
        color: #fff;
        background: #ffa500;
    }

    label {
        font-family: 'Ubuntu', sans-serif;
        display: block;
        padding: 5px;
        font-size: 1.5em;
    }
    .inputfield {
        font-family: 'Ubuntu', sans-serif;
        margin: auto;
        display: block;
        padding: 5px;
        border: none;
        font-size: 22px;
    }

</style>