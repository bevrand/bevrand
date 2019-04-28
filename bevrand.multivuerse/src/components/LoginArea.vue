<template>
    <div class="loginarea">
        <h2>Welcome!</h2>
        <form id="loginForm" @submit="checkLoginForm">
            <section class="inputarea">
                <input
                    type="text"
                    placeholder="Username"
                    class="inputfield"
                    v-model="username"
                    id="username"
                />
                <br />
                <input type="email"
                       v-model="email"
                       placeholder="Email"
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
                <button v-if="!loggingIn"
                        id="loginButton"
                        class="loginbutton">Login
                </button>
                <h4>Don't have an Account?</h4>
                <router-link
                        tag="a"
                        id="navlinkRegister"
                        :to="{ name: 'registerPage' }">
                    Sign up here!
                </router-link>
                <circles-to-rhombuses-spinner v-if="loggingIn"
                        :animation-duration="1200"
                        :circles-num="4"
                        :circle-size="15"
                        color="#ff9500"
                        class="spinner"
                />
            </section>
        </form>
    </div>
</template>

<script>
    import { CirclesToRhombusesSpinner } from 'epic-spinners'

    export default {
        name: "LoginArea",
        data() {
            return {
                email: '',
                password: '',
                username: '',
                token: '',
                loggingIn: false,
                count: 2
            }
        },
        components: {
            CirclesToRhombusesSpinner
        },
        methods: {
            checkLoginForm: function (e) {
                if(!this.email || !this.password) {
                    this.alert("Missing a required field")
                }
                else {
                    this.loggingIn = true;
                    this.count = 2;
                    this.login()
                }
                e.preventDefault();
            },

            login: function () {
                this.$apiClient({
                    method: 'post',
                    url: `${this.$proxyUrl}/authentication-api/login`,
                    data: {
                        "emailAddress" : this.emailAddress,
                        "password": this.password,
                        "username": this.username
                    }
                })
                    .then((response) => {
                        this.token = response.data['token'];
                        this.$store.commit('setToken', response.data);
                        window.setInterval(() => {
                            if (this.count === 0) {
                                this.loggingIn = false;
                                this.$router.push({name: 'profilePage', params: {username: this.username}});
                            }
                            this.count--;
                        }, 1000);
                    })
                    .catch(e => {
                        window.setInterval(() => {
                            if (this.count === 0) {
                                this.loggingIn = false;
                                this.alert("Login failed")
                            }
                            this.count--;
                        }, 1000);
                    })
            },
            alert: function(text){
                this.$swal("Something went wrong", text, "error")
            },
        }
    }
</script>


<style scoped>
    .inputarea {
        margin: 2em 22em 1em;
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

    #loginButton {
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

    #loginButton:hover {
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

    .spinner {
        margin-top: 2em;
        margin-bottom: 4em;
        margin-left: 45%;
        text-align: center;
    }

    @media screen and (max-width: 1366px) {
        .spinner {
            margin: 2em 10em 3em 35%;
            text-align: center;
        }
    }

    @media screen and (max-width: 650px) {
        .spinner {
            margin: 1em 1em 2em 30%;
            text-align: center;
        }
    }

</style>