import { formatTwoDecimals } from "@/utils/common.js"
import {r_getAllProducts,getAllCategories,getUpdatedProducts,getEmployeeDetails} from "../repo/SaleRepo.js"
import { notify_failed } from "@/utils/notifications.js"
import { bulkAddRecord, ensureOpenDB, addRecord, p_getAllFromTable, p_openDB, queryTable, p_queryTable, p_updateTable, p_addRecord } from "@/repo/LocalDB.js"
import { r_checkFeatureFlag } from "@/repo/AuthorizationRepo.js"
import { checkFlag } from "@/repo/FeatureFlagsRepo.js"

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
      // iterate state and update if product is in the product updates
      state.products.forEach((product, index) => {
          // Update the state 
          if (product.ref in productUpdates){
              // Update the product 
              state.products[index] = productUpdates[product.ref]
          }
      });

      // Update the indexedDb
      for (let key in productUpdates){
          let product = productUpdates[key]
          p_updateTable('products','refIndex',key,product)
      }
    },
    updateAddedProduct(state, productUpdates) {
      // Iterate over the incoming updates
      Object.values(productUpdates).forEach(newProduct => {
        // Check if the product already exists in state
        const exists = state.products.some(p => p.ref === newProduct.ref);
        
        if (!exists) {
          // Add it if it doesn't exist
          state.products.push(newProduct);
          // Add the product to the indexedDb 
          p_addRecord('products',newProduct)
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
     async fetchAllProducts({commit}){
        
        const featureEnabled = await checkFlag('local-products-caching')

        // #region FETCH FROM LOCAL DB (FLAG ENABLED)
        if (featureEnabled){
            // Ensure database connection 
            await ensureOpenDB()

            // Get last fetched result
            let last_fetched = await p_queryTable('config','keyIndex',IDBKeyRange.only('last_fetched'))

            // Never fetched before
            if (last_fetched.length == 0){
                // On products received 
                let onProductsReceived = (success,payload)=>{
                    // Failed 
                    if (!success){
                        // If 401 received then dont notify 
                        if (payload.response && payload.response.status === 401){
                          return
                        }

                        // Notify failed to fetch from server
                        notify_failed("Failed to fetch products from server")
                        return
                    }

                    // Set the products in vuex 
                    commit('setProducts',payload.products)
                    commit('setLastFetchedTimestamp',payload.timestamp)

                    // Set the last updated in local db 
                    addRecord('config',{
                        key: 'last_fetched',
                        value: payload.timestamp
                    })

                    // Insert products into the local database
                    payload.products.forEach(product => {
                        addRecord('products',product,(success,payload)=>{
                            if (!success){
                              console.log('Failed to write record to db',product)
                            }
                        })
                    })

                    return
                }

                // Fetch from server
                r_getAllProducts(onProductsReceived)
                return
            }

            // Query the product 
            let products = await p_getAllFromTable('products')
            products.sort((a, b) => new Date(b.last_upated) - new Date(a.last_upated));

            // Set the products in vuex 
            commit('setProducts',products)
            commit('setLastFetchedTimestamp',last_fetched[0].value)

            // Fetch updates from the database 
            this.dispatch('sales/fetchProductUpdates')
            return
       }
       //#endregion

       //#region FETCH PRODUCTS FROM SERVER 
       let onProductsReceived = (success,payload)=>{
          // Failed 
          if (!success){
              // If 401 received then dont notify 
              if (payload.response && payload.response.status === 401){
                return
              }

              // Notify failed to fetch from server
              notify_failed("Failed to fetch products from server")
              return
          }

          // Set the products in vuex 
          commit('setProducts',payload.products)
          commit('setLastFetchedTimestamp',payload.timestamp)
        }
        
       r_getAllProducts(onProductsReceived)
       //#endregion
     },
     // Fetch all categories
     async fetchAllCategories({commit}){
        // Local cache feature flag 
        const localFeatureFlag = await checkFlag('local-categories-caching')


        //#region LOCAL CACHE GET
        if (localFeatureFlag){
            // Ensure database connection 
            await ensureOpenDB()

            // Get last fetched result
            let last_fetched = await p_queryTable('config','keyIndex',IDBKeyRange.only('last_fetched'))

            // Categories are in the database 
            if (last_fetched.length > 0){
                p_getAllFromTable('categories').then(categories => {
                    // Set the products  
                    commit('setCategories',categories)
                })
                return
            }

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
                
                // Save categories in the database
                payload.categories.forEach(category => {
                    p_addRecord('categories',category)
                })

                // Set the catories
                commit('setCategories',payload.categories)
            }

            // Fetch categories
            getAllCategories(onCategoriesReceived)

            return
        }
        //#endregion

        //#region ALWAYS FETCH FROM SERVER
        let onCategoriesReceived = (success,payload)=>{
            // Failed 
            if (success === false){
                // If 401 received then dont notify 
                if (payload.response && payload.response.status === 401){
                  return
                }

                return notify_failed("Failed to fetch product categories from backend")
            }

            // Set the catories
            commit('setCategories',payload.categories)
        }

        // Fetch categories
        getAllCategories(onCategoriesReceived)

        //#endregion
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

            // Update the last_updated timestamp 
            state.lastFetchedTimestamp = payload.timestamp
            
            p_updateTable('config','keyIndex','last_fetched',{
                value: payload.timestamp,
                key: 'last_fetched'
            })
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