<template>
    <div class="sales-wrapper">
        <!-- Tool Bar  -->
        <ToolBar @on_search_text_changed="onSearchTextChanged" @refresh-page="refreshPage" />

        <!-- bottom  -->
        <div class="bottom">
            <!-- left -->
            <div class="left">
                <div class="categories">
                    <div class="category-wrapper" :key="category.ref" v-for="category in categories">
                        <StockCategory 
                            :name="category.name"
                            :stock_count="category.stock_count"
                            :icon="category.icon"
                            :ref="category.ref"
                            :selected="selected_category === category.ref"
                            @click="()=>selected_category = category.ref"/>
                    </div>
                </div>
                <div class="products">
                    <div class="product-wrapper" :key="product.ref" v-for="product in filtered_products">
                        <Product
                            :name="product.name"
                            :description="product.description"
                            :stock="product.in_stock"
                            :product_ref="product.ref"
                            :price="this.$store.state.currency === 'ZWG' ? product.price_zwg : product.price_usd"
                            :image="product.image_url"
                            v-on:on_update_product="(e)=>onCartProductUpdate(product,e)"/>
                    </div>
                </div>  
                <br>
                <br>                                                                
            </div>
            <!-- Right -->
            <div class="right">
                <SidePanel 
                    :cart_products="this.$store.getters['cart/cart_products']"
                    :proccessing="submitting_cart" 
                    @complete-cart="onCompleteCart"
                    @on-payment-method-change="setPaymentMethod"/>
            </div>
        </div>

    </div>
</template>

<style lang="css" scoped>
    .sales-wrapper {
        width: 100%;
        height: 100vh;
        overflow-y: hidden;
    }

    .tool-bar {
        background-color: white;
        height: 45px;
        max-height: 45px;
        padding-left: 20px;
        padding-top: 10px;
        padding-bottom: 10px;
        border-bottom: solid 1.8px rgba(128, 128, 128, 0.116);
        display: grid;
        grid-template-columns: 0.78fr 0.03fr 0.05fr 0.1fr;
    }

    .search-box-wrapper{
        display: flex;
        align-items: center;
        margin-left: 20%;
    }
    .notification-icon-wrapper, .currency-icon-wrapper {
       display: flex;
       justify-content: center;
       align-items: center;
    }

    img.bell {
        height: 15px;
        width: 15px;
    }

    .profile-wrapper {
        display: grid;
        grid-template-columns: 35px auto;
        grid-column-gap: 5px;
    }

    .profile-wrapper .dp img {
        border-radius: 50%;
        height: 35px;
        width: 35px;
    }

    .profile-wrapper .content {
        display: flex;
        justify-content: center;
        transform: translateY(-1px);
    }
    .profile-wrapper .content .fullname {
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 1px;
        margin-top: auto;
    }

    .profile-wrapper .content .title{
        font-size: 0.7rem;
    }

    .align-center {
        margin-top: auto;
        margin-bottom: auto;
    }

    .bottom {
        display: grid;
        padding: 20px;
        padding-top: 10px;
        grid-template-columns: calc(100% - 350px) 350px;
        height: calc(100vh - 65px);
    }

    .bottom .left {
        height: inherit;
        overflow-y: scroll;
    }

    .bottom .left::-webkit-scrollbar{
        display: none;
    }

    .categories {
        display: flex;
        flex-wrap: wrap;
        gap: 5px 10px;
        width: 100%;
    }

    .products {
        padding-top: 20px;
        display: flex;
        flex-wrap: wrap;
        column-gap: 10px;
        row-gap: 10px;
    }
    
    @media only screen and (max-width: 1200px) {
        .bottom {
            grid-template-columns: auto 240px;
        }
        
        .tool-bar {
            background-color: white;
            height: 45px;
            max-height: 45px;
            padding-left: 20px;
            padding-top: 10px;
            padding-bottom: 10px;
            border-bottom: solid 1.8px rgba(128, 128, 128, 0.116);
            display: grid;
            grid-template-columns: 0.8fr 0.05fr 0.05fr 0.2fr;
        }

        .search-box-wrapper{
            width: 100%;
            margin-left: 0%;
        }
    }

    @media only screen and (max-width: 1000px) {
        .bottom {
            grid-template-columns: auto 220px;
        }
    }

</style>

<script>
    import LeftIconedInput from "../../components/LeftIconedInput"
    import TwinSelector from "@/components/TwinSelector.vue";
    import StockCategory from "@/components/StockCategory.vue";
    import Product from "@/components/Product.vue";
    import SidePanel from "@/components/SidePanel.vue";
    import { completeCart } from "@/repo/SaleRepo";
    import ProductModel from "@/models/ProductModel";
    import { generateUUID } from "@/utils/common";
    import { notify_success, notify_cart_completed } from "@/utils/notifications";
    import ToolBar from "@/components/ToolBar.vue";
    
    export default {
        name: "SalesTab",
        components: {
            LeftIconedInput,
            TwinSelector,
            StockCategory,
            Product,
            SidePanel,
            ToolBar
        },
        data(){
            return {
                selected_category: '*',
                search_text : '',
                submitting_cart: false,
                idempotence_key : null,
                payment_method : 'swipe'
            }
        },
        mounted(){
            this.init()
        },
        methods: {
            init(){
                this.idempotence_key = generateUUID()
            },
            refreshPage(){
                this.$emit("refresh-page")
            },
            onCartProductUpdate(product,count){
                if (count > 0){
                    this.$store.commit('cart/addProduct',product)
                }
                else {
                    this.$store.commit('cart/removeProduct',product)
                }
            },
            onCurrencyChange(index){
                if (index === 0){
                    this.$store.commit('setCurrency', 'USD')
                }
                else {
                    this.$store.commit('setCurrency', 'ZWG')       
                }
            },
            setPaymentMethod(payload){
                this.payment_method = payload
            },
            onSearchTextChanged(searchText){
                this.selected_category = '*'
                this.search_text = searchText
            },
            onCartCompleted(success,payload){
                // Stop the loading 
                this.submitting_cart = false

                // Generate new idempotance key 
                this.idempotence_key = generateUUID()
                
                // log the event
                this.$store.dispatch('cart/clearCart')

                // Notify cart completed 
                notify_cart_completed()
                
                // Notify the client
                notify_success(`Completed cart - ${payload.ref}`)
            },
            onCompleteCart(){
                // Show progress 
                this.submitting_cart = true

                // Submit cart
                let listOfProductModel = this.$store.getters['cart/cart_products_as_individual_list'].map(product => {
                    return new ProductModel()
                        .setId(product.id)
                        .setRef(product.ref)
                        .setFetched(product.fetched)
                        .setName(product.name)
                        .setCategoryRef(product.category.ref)
                        .setDescription(product.description)
                        .setInStock(product.in_stock)
                        .setPriceUsd(product.price_usd)
                        .setPriceZwg(product.price_zwg)
                        .setLastUpdated(product.last_updated)
                })

                // Complete the cart 
                completeCart(
                    this.onCartCompleted,
                    listOfProductModel,
                    this.$store.state.currency,
                    this.idempotence_key,
                    this.payment_method,
                    this.$store.state.sales.employee.username,
                    this.$store.state.sales.employee.shop.ref
                )
            
            }
        },
        computed: {
            filtered_products(){
                
                // Filter with search text 
                let products = this.$store.state.sales.products.filter(product => {
                    return product.name.toLowerCase().includes(this.search_text.toLowerCase()) ||
                        product.description.toLowerCase().includes(this.search_text.toLowerCase()) || 
                        product.category.name.toLowerCase().includes(this.search_text.toLowerCase())
                })

                // Return all products if the filter is a wildcard
                if (this.selected_category === '*'){
                    return products
                }

                // Return only products in the cart if selected is cart 
                if (this.selected_category === 'cart'){
                    return products.filter(product => product.ref in this.$store.getters['cart/cart_products_references_set'])
                }

                // Return from selected cateogry
                return products.filter(product => product.category.ref === this.selected_category)
            },
            categories(){
                return this.$store.state.sales.categories
            }
        }
    }
</script>