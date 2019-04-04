// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import axios from 'axios';
import VueCarousel from 'vue-carousel';
import vueSmoothScroll from 'vue2-smooth-scroll';
import VueAlertify from 'vue-alertify';

Vue.config.productionTip = false;

Vue.http = Vue.prototype.$apiClient = axios;

Vue.use(vueSmoothScroll);
Vue.use(VueAlertify);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store,
  VueCarousel,
  template: '<App/>'
}).$mount('#app');

