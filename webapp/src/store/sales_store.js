import {getAllProducts,getAllCategories} from "../repo/SaleRepo.js"
import { notify_failed } from "@/utils/notifications.js"

export default {
  namespaced: true,
  // State 
  state: () => ({
    products: [],
    categories: []
  }),
  // Mutations
  mutations: {
    setProducts(state, products) {
        state.products = products
    },
    setCategories(state,categories){
        state.categories = categories
    }
  },
  // Actions
  actions: {
     // Fetch products from the database 
     fetchAllProducts({commit}){

        // Callback on products received 
        let onProductsReceived = (success,payload)=>{
            // Failed 
            if (success === false){
                notify_failed(payload)
                return
            }

            // Set the products  
            commit('setProducts',payload)
        }

        // Fetch products 
        getAllProducts(onProductsReceived)
     },
     // Fetch all categories
     fetchAllCategories({commit}){
        // Callback on categories received
        let onCategoriesReceived = (success,payload)=>{
            // Failed 
            if (success === false){
                notify_failed(payload)
                return
            }

            // Set the products  
            commit('setCategories',payload)
        }

        // Fetch categories
        getAllCategories(onCategoriesReceived)
     }


  },
  // Getters 
  getters: {
    
  },
}