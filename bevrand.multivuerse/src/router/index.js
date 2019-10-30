import Vue from 'vue'
import Router from 'vue-router'
import store from '../store';

Vue.use(Router);

function guard(to, from, next){
    if(store.state.loggedIn) {
        next(); // allow to enter route
    } else{
        next('/login'); // go to '/login';
    }
}

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'homepage',
            component: () => import("../views/HomePage"),
            props: {
                playlist: true
            }
        },
        {
            path: '/login/',
            name: 'loginPage',
            component: () => import("../views/Login")
        },
        {
            path: '/register/',
            name: 'registerPage',
            component: () => import("../views/Register")
        },
        {
            path: '/profile/',
            name: 'profilePage',
            component: () => import("../views/Profile")
        },
        {
            path: '/reroute/:username',
            beforeEnter: guard,
            name: 'reroutePage',
            component: () => import("../views/ReRoutePage")
        },
        {
            path: '/pictures',
            beforeEnter: guard,
            name: 'picturePage',
            component: () => import("../views/Pictures"),
        },
        {
            path: '/playlistcreation/:displayName',
            name: 'playlistCreationPage',
            component: () => import("../views/PlaylistCreationPage")
        },
        {
            path: '/editplaylist/',
            name: 'editPlaylistPage',
            component: () => import("../views/EditPlaylist"),
            props: {
                playlist: true
            }
        },
        {
            path: '/playlistdetails/',
            name: 'playlistDetailPage',
            component: () => import("../views/PlaylistDetail"),
            props: {
                playlist: true
            }
        },
    ]
})