import { formatTwoDecimals } from "@/utils/common.js"
import {getAllProducts,getAllCategories,getUpdatedProducts,getEmployeeDetails} from "../repo/SaleRepo.js"
import { notify_failed } from "@/utils/notifications.js"

export default {
  namespaced: true,
  // State 
  state: () => ({
    products: [],
    categories: [],
    lastFetchedTimestamp: null,
    employee: {
        name: null,
        role: null
    }
  }),
  // Mutations
  mutations: {
    setProducts(state, products) {
        state.products = products
    },
    setCategories(state,categories){
        state.categories = categories
    },
    setLastFetchedTimestamp(state,timestamp){
        state.lastFetchedTimestamp = timestamp
    },
    updateProducts(state,productUpdates){
      // iterate products
      state.products.forEach((product, index) => {
          if (product.ref in productUpdates){
              // Update the product 
              state.products[index] = productUpdates[product.ref]
          }
      });
    },
    updateAddedProduct(state, productUpdates) {
      // Iterate over the incoming updates
      Object.values(productUpdates).forEach(newProduct => {
        // Check if the product already exists in state
        const exists = state.products.some(p => p.ref === newProduct.ref);
        
        if (!exists) {
          // Add it if it doesn't exist
          state.products.push(newProduct);
        }
      });
    },
    setEmployee(state,employee){
      state.employee = employee
    }
  },
  // Actions
  actions: {
     // Fetch employee details 
     fetchEmployeeDetails({commit}){
        // callback 
        let onEmployeeDetailsReceived = (success,payload)=>{
            if (!success){
              // If 401 received then dont notify 
              if (payload.response && payload.response.status === 401){
                return
              }

              notify_failed("Failed to fetch employee details from server")
              return
            }

            // Commit the employee
            commit('setEmployee',payload.employee)
        }

        // Set employee details
        getEmployeeDetails(onEmployeeDetailsReceived)
     },
     // Fetch products from the database 
     fetchAllProducts({commit}){

        // Callback on products received 
        let onProductsReceived = (success,payload)=>{
            // Failed 
            if (success === false){
                // If 401 received then dont notify 
                if (payload.response && payload.response.status === 401){
                  return
                }


                notify_failed("Failed to fetch products from server")
                return
            }

            // Set the products  
            commit('setProducts',payload.products)
            commit('setLastFetchedTimestamp',payload.timestamp)
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
                // If 401 received then dont notify 
                if (payload.response && payload.response.status === 401){
                  return
                }

                return notify_failed("Failed to fetch product categories from backend")
            }

            // Set the products  
            commit('setCategories',payload.categories)
        }

        // Fetch categories
        getAllCategories(onCategoriesReceived)
     },
     // Fetch new product updates
     fetchProductUpdates({commit,state},productAdded){
        // callback on products received
        let onProductsReceived = (success,payload)=>{
            // Failed 
            if (success === false){
                notify_failed(payload)
                return
            }

            // Set the products
            if (productAdded){
                return commit('updateAddedProduct',payload.products)
            }
            
            // Updated products
            commit('updateProducts',payload.products)
            
        }

        getUpdatedProducts(onProductsReceived,state.lastFetchedTimestamp)
     }
  },
  // Getters 
  getters: {
      get_products_list(state){
         return state.products.map(product => {
            return {
                ...product,
                price_usd : formatTwoDecimals(product.price_usd),
                price_zwg : formatTwoDecimals(product.price_zwg)
            }
         })
      }
    
  },
}