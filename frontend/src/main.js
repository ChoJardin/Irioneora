import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import VueCookies from 'vue-cookies'
import VModal from 'vue-js-modal'

Vue.config.productionTip = false

Vue.use(VueCookies)
Vue.use(VModal, { dynamic: true })

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
