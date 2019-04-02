import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        title: 'MultiVuerse',
        token: "",
        selectedPlaylist: 'Please select a playlist',
        lastUpdated: null
    }
})