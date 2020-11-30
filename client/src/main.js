import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import router from "./router";
import store from "./store";
import '../public/main.css';
import 'bootstrap/dist/css/bootstrap.min.css'
// Install BootstrapVue
Vue.use(BootstrapVue)
import VueCookies from 'vue-cookies'
Vue.use(VueCookies)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
