import Vue from 'vue'
import App from './App'

import cuCustom from './components/cu-custom.vue'
Vue.component('cu-custom',cuCustom)

Vue.config.productionTip = false


App.mpType = 'app'
import store from "./store"

const app = new Vue({
	store,
    ...App
})
app.$mount()
