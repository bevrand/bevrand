import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        token : null,
        loggedIn: false,
        username: "",
        id: "",
        email: "",
        jwtData: null,
        proxyUrl: process.env.ROOT_PROXY_API
    },
    mutations: {
        setToken : (state, authResponse) => {
            state.token = authResponse['token'];
            state.jwtData =  JSON.parse(atob(authResponse['token'].split('.')[1]));
            state.username = state.jwtData.username;
            state.id = state.jwtData.id;
            state.loggedIn = true;
        }
    }
})