<template>
    <div class="loginarea">
        <h2>Welcome!</h2>
        <form id="loginForm" @submit="checkLoginForm">
            <section class="inputarea">
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
                <button
                        id="loginButton"
                        class="loginbutton">Login
                </button>
            </section>
        </form>
    </div>
</template>

<script>
    export default {
        name: "LoginArea",
        data() {
            return {
                email: '',
                password: '',
                token: '',
            }
        },

        methods: {
            checkLoginForm: function (e) {
                if(!this.email || !this.password) {
                    this.alert("Missing a required field")
                }
                else {
                    this.login()
                }
                e.preventDefault();
            },

            login: function () {
                this.alert("logged in")
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


    #loginButton {
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

    #loginButton:hover {
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