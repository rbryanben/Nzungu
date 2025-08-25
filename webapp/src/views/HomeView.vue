<template>
  <div class="wrapper">
      <div class="tiles">
          <div class="tile" :class="{'selected' : selected === 'sale'}" @click="select('sale','sales')"  title="Make Sale">
              <img src="/svg/shopping-basket-white.svg" alt="">
          </div>
          <div class="tile" :class="{'selected' : selected === 'my-sales'}" @click="select('my-sales','view-sales')"  title="My Sales">
              <img src="/svg/wallet.svg" alt="">
          </div>
          <div class="tile" :class="{'selected' : selected === 'inventory'}" @click="select('inventory','inventory')"  title="Shop Inventory">
              <img src="/svg/cart-flatbed.svg" alt="">
          </div>
          <div class="tile" :class="{'selected' : selected === 'logout'}" @click="logout"  title="Logout">
              <img src="/svg/arrow-right-from-bracket.svg" alt="">
          </div>
      </div>
      <div class="panel">
          <router-view @refresh-page="onRefreshPage" />
      </div>
  </div>
</template>

<style lang="css" scoped>
  .wrapper {
    display: grid;
    grid-template-columns: 50px calc(100vw - 50px) ;
    background-color: #f2f1f2;
    height: 100vh;
    width: 100vw;
  }

  .tiles {
   height: 100vh;
   z-index: 10;
   background-color: white;
   border-right: solid 1.8px rgba(225, 225, 225, 0.116);
   width: 100%;
   cursor: pointer;
   transition: all 0.2s ease-in;
  }
  
  .tile {
    margin-top: 10px;
    display: flex;
    position: relative;
    background-color: rgba(182, 182, 182, 0.881);
    width: 30px;
    height: 30px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 8px;
    transition: all 0.1s ease-in;
  }

  .tile.selected {
    background-color: rgba(243, 138, 27, 0.86);
  }

  .tile img {
    width: 18px;
    height: 18px;
    margin: auto;
    object-fit: contain;
  }

  @media only screen and (max-width: 1200px) {
    .tile img {
      width: 15px;
      height: 15px;
      margin: auto;
    }
  }
</style>

<script>

  // Libraries
  import {io} from "socket.io-client"
  import { ENDPOINTS } from "@/main"
  import { getAuthorizationToken } from "@/repo/AuthorizationRepo"
  import { completeCart } from "@/repo/SaleRepo"
  import { notify_failed, notify_success } from "@/utils/notifications"
  import ProductModel from "@/models/ProductModel"

  export default {
      name: "SaleView",
          data(){
            return {
                socketioClient : null,
                selected: 'sale'
            }
          },
          methods: {
              init(){
                // Fetch categories from the database 
                this.$store.dispatch('sales/fetchAllCategories')
                // Fetch products from the database 
                this.$store.dispatch('sales/fetchAllProducts')
                // Fetch employee details
                this.$store.dispatch('sales/fetchEmployeeDetails')
                // Setup socket io client
                this.socketioClient =  io(ENDPOINTS.LIVE_UPDATES_ENDPOINT,{
                    extraHeaders: {
                        "Authorization" : getAuthorizationToken()
                    }
                })

                // Create the client
                this.socketioClient.on('connect',this.onSocketConnnect)
                this.socketioClient.on('disconnect',this.onSocketDisconnected)
                this.socketioClient.on('on-event',this.onSocketEvent)
              },
              onRefreshPage(){
                this.init()
              },
              select(name,route){
                this.selected = name
                this.$router.push({name : route})
              },
              onSocketConnnect(){
                 notify_success('Connected to live updates service')
              },
              onSocketDisconnected(){
                 notify_failed('Disconnected from live updates service')
              },
              onSocketEvent(payload){
                  // Update products list 
                  if ('event' in payload && new Set(['product-updated', 'product-stock-updated', 'cart-completed']).has(payload.event)){
                    // Dispatch the call to update products
                    this.$store.dispatch('sales/fetchProductUpdates',false)
                    return
                  }
                  
                  // Product added 
                  if ('event' in payload && payload.event === 'product-added'){
                    // Dispatch the call to update products
                    this.$store.dispatch('sales/fetchProductUpdates',true)  
                    // Fetch category updates
                    this.$store.dispatch('sales/fetchAllCategories')
                    return
                  }

              },
              submitOfflineSales(){
                  // context
                  const context = this

                  // Check if there are offline sales 
                  const offlineSales = localStorage.getItem('LOCAL_SALES_CACHE')
                  // If object-fi
                  localStorage.setItem('LOCAL_SALES_CACHE','[]')

                  // If null then return 
                  if (offlineSales === null){
                      return
                  }

                  // Parse the sales
                  let obj_offlineSales = []
                  try{
                    obj_offlineSales = JSON.parse(offlineSales)
                  }

                  catch(error){
                     localStorage.setItem('LOCAL_SALES_CACHE_FAILED',JSON.stringify(offlineSales))
                     return
                  }

                  // If not a list then register as failed
                  if (Array.isArray(obj_offlineSales) === false){
                      localStorage.setItem('LOCAL_SALES_CACHE_FAILED',JSON.stringify(obj_offlineSales))
                      return
                  }

                  // Submit the products
                  obj_offlineSales.forEach(sale => {
                      // Products as products list 
                      const productsAsListOfProductModel = sale.cart_items.map(product => {
                        return  new ProductModel()
                                    .setId(product.id)
                                    .setRef(product.ref)
                                    .setFetched(product.fetched)
                                    .setName(product.name)
                                    .setCategoryRef(product.category_ref)
                                    .setDescription(product.description)
                                    .setInStock(product.in_stock)
                                    .setPriceUsd(product.price_usd)
                                    .setPriceZwg(product.price_zwg)
                                    .setLastUpdated(product.last_updated)
                      })
                     
                      completeCart(
                        context.onOfflineSubmitted,
                        productsAsListOfProductModel,
                        sale.currency,
                        sale.idempotence_key,
                        sale.payment_option,
                        sale.teller,
                        sale.shop
                      )
                  });

              },
              logout(){
                  // Clear any cart 
                  this.$store.dispatch('cart/clearCart')
                  // Clear authorization token
                  localStorage.removeItem('authorization')
                  window.location.replace('/login')
              }
          },
          mounted(){
              this.init()
              // Set a background task for submitting sales
              setInterval(this.submitOfflineSales,15 * 1000)
          }
  }
</script>