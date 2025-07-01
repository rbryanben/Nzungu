import { createStore } from 'vuex'
import sales_store from './sales_store'

export default createStore({
  state: { 
     name : "yayy vuex is working"
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    sales : sales_store
  }
})
