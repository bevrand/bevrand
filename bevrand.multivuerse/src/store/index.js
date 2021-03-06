import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        token : null,
        storedDrinksFromPicture: [],
        creationPlaylistBeverages: [],
        creationPlaylistDisplayname: "",
        loggedIn: false,
        username: "",
        id: "",
        email: "",
        jwtData: null,
        proxyUrl: document.location.origin
    },
    mutations: {
        setToken : (state, authResponse) => {
            state.token = authResponse['token'];
            state.jwtData =  JSON.parse(atob(authResponse['token'].split('.')[1]));
            state.username = state.jwtData.username;
            state.id = state.jwtData.id;
            state.loggedIn = true;
            localStorage.setItem('token', authResponse['token']);
        },

        getTokenFromStorage: (state) => {
            if (localStorage.getItem("token") === null || localStorage.getItem("token") === 'null') {
                return
            }
            let token = localStorage.getItem('token');
            state.token = token;
            state.jwtData =  JSON.parse(atob(token.split('.')[1]));
            state.username = state.jwtData.username;
            state.id = state.jwtData.id;
            state.loggedIn = true;
        },

        logOut: (state) => {
            state.token = null;
            state.jwtData =  null;
            state.username = null;
            state.id = null;
            state.loggedIn = false;
            localStorage.setItem('token', null);
        },

        setDrinksFromPicture: (state, drinks) => {
            state.storedDrinksFromPicture = drinks;
        },
        setPlaylistCreationName: (state, displayName) => {
            state.creationPlaylistDisplayname = displayName;
        },
        setPlaylistBeverages: (state, beverages) => {
            state.creationPlaylistBeverages = beverages;
        },
        emptyStoredBeverages: (state) => {
          state.storedDrinksFromPicture = [];
          state.creationPlaylistBeverages = [];
        },
    },

    getters : {
        reRouteIfNotLoggedIn: state => state.loggedIn
    }
})