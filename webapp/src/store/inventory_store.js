import { notify_failed } from "@/utils/notifications.js"
import { getFilters, getProductsInventory } from "@/repo/ProductsRepo"

export default {
  namespaced: true,
  // State 
  state: () => ({
    products: [],
    filters: [],
    last_fetched: null
  }),
  // Mutations
  mutations: {
    setProducts(state,products){
        state.products = products
    },
    setFilters(state,filters){
      state.filters = filters.filters
      state.last_fetched = filters.timestamp
    }
  },
  // Actions
  actions: {
    fetchInventory({commit}){
        // Callback on inventory received
        let onInventoryReceived = (success,payload)=>{
            console.log(payload)
            // Failed 
            if (success === false){
                notify_failed(payload)
                return
            }

            // Set the products  
            commit('setProducts',payload)
        }

        // Fetch categories
        getProductsInventory(onInventoryReceived)
    },
    fetchFilters({commit}){
        let onFiltersReceived = (success,payload)=>{
          // Failed 
          if (success === false){
              notify_failed(payload)
              return
          }

          // Set the filters
          commit('setFilters',payload)
        }

        // Fetch the filters from the backend
        getFilters(onFiltersReceived)
    }
  },
  // Getters 
  getters: {
    get_inventory(state){
        return state.products   
    },
    get_filters(state){
      return state.filters
    }
  },
}