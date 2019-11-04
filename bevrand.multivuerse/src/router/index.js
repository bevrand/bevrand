import Vue from 'vue'
import Router from 'vue-router'
import store from '../store';

Vue.use(Router);

async function guard(to, from, next) {
    try {
        let hasPermission = false;
        let times = 10;
        let time = 0;

        while (time < times && !hasPermission) {
            hasPermission = await store.getters["reRouteIfNotLoggedIn"];
            time++
        }
        if (hasPermission) {
            next()
        }
        else {
            next({
                name: "loginPage" // back to safety route //
            })
        }
    } catch (e) {
        next({
            name: "homepage" // back to safety route //
        })
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
            beforeEnter: guard,
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
            beforeEnter: guard,
            name: 'playlistCreationPage',
            component: () => import("../views/PlaylistCreationPage")
        },
        {
            path: '/editplaylist/',
            beforeEnter: guard,
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