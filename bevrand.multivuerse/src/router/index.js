import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'homepage',
            component: () => import("../views/HomePage")
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
            name: 'reroutePage',
            component: () => import("../views/ReRoutePage")
        },
    ]
})
