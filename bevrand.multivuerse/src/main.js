// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import axios from 'axios';
import VueCarousel from 'vue-carousel';
import vueSmoothScroll from 'vue2-smooth-scroll';
import VueSwal from 'vue-swal'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faPencilAlt,
  faTrash,
  faPlusCircle,
  faDice,
  faGlassMartini,
  faGlassWhiskey,
  faBeer,
  faCodeBranch,
  faArrowAltCircleDown,
  faArrowAltCircleUp,
  faCamera,
  faQuestion
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faPencilAlt, faTrash, faPlusCircle, faDice, faGlassMartini, faCodeBranch, faGlassWhiskey,
    faBeer, faArrowAltCircleDown, faArrowAltCircleUp, faQuestion, faCamera);

Vue.config.productionTip = false;

Vue.http = Vue.prototype.$apiClient = axios;
Vue.prototype.$proxyUrl = store.state.proxyUrl;

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.use(vueSmoothScroll);
Vue.use(VueSwal);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store,
  VueCarousel,
  template: '<App/>'
}).$mount('#app');

