import { notify_failed } from "@/utils/notifications.js"

export default {
  namespaced: true,
  // State 
  state: () => ({
    working_cart: {}
  }),
  // Mutations
  mutations: {
    addProduct(state,product) {
        // Not in cart create an entry
        if (!state.working_cart[product.ref]){
            state.working_cart[product.ref] = {
                product : product,
                count : 1,
                updated: new Date().toISOString()
            }
            return
        }
        
        // Increment the product count 
        if (state.working_cart[product.ref] && state.working_cart[product.ref].count){
            state.working_cart[product.ref].count += 1
        } 
    },
    removeProduct(state,product){
        // If there is already nothing in the cart do nothing
        if (!state.working_cart[product.ref]) {
            return;
        }

        const item = state.working_cart[product.ref];

        // If there's only one item left, remove the key from the cart
        if (item.count === 1) {
            delete state.working_cart[product.ref];
            return;
        }

        // Subtract the count by 1
        item.count -= 1;
    }
  },
  // Actions
  actions: {
     
  },
  // Getters 
  getters: {
    cart_products(state){
        let cart_items = Object.keys(state.working_cart).map(cart_key => {
            
            // Item in iteration
            let item = state.working_cart[cart_key]
            
            // Return neccessary data 
            return {
                name : item.product.name,
                description : item.product.description,
                cart_count : item.count,
                category_name : item.product.category.name,
                product_price_usd : item.product.price_usd,
                product_price_zwg : item.product.price_zwg,
                updated : item.updated,
                image_url : item.product.image_url
            }
        }).sort((a, b) => new Date(b.updated) - new Date(a.updated))

        return cart_items
    },
    cart_subtotal(state){
        let subTotal_zwg = 0 ;
        let subTotal_usd = 0 ;

        Object.keys(state.working_cart).forEach(cart_key => {
            let item = state.working_cart[cart_key]   
            subTotal_zwg += item.product.price_zwg * item.count
            subTotal_usd += item.product.price_usd * item.count
        });

        return {
            subtotal_zwg :  subTotal_zwg.toFixed(2),
            subtotal_usd : subTotal_usd.toFixed(2),
            tax_zwg : 0,
            tax_usd : 0
        }
    },
    cart_products_references_set(state){
        // Set to return 
        let referenceSet = {}

        Object.keys(state.working_cart).forEach(cart_key => {
            let item = state.working_cart[cart_key]   
            referenceSet[item.product.ref] = item.count
        });

        return referenceSet
    },
    cart_products_as_individual_list(state){
        
        // List to return  
        let cart_list = []

        // Add products 
        Object.keys(state.working_cart).forEach(cart_key => {
            let item = state.working_cart[cart_key]  
            // Add items 
            for (let i = 0; i < item.count; i++) {
                cart_list.push(item.product);
            }
        });

        return cart_list
    }
  },
}