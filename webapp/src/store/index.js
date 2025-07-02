import { createStore } from 'vuex'
import sales_store from './sales_store'
import cart_store from './cart_store'

export default createStore({
  state: { 
     currency: "USD"
  },
  getters: {
  },
  mutations: {
     setCurrency(state, newCurrency) {
      state.currency = newCurrency;
    }
  },
  actions: {
  },
  modules: {
    sales : sales_store,
    cart : cart_store
  }
})
