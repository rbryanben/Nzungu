<template>
    <div class="inventory-wrapper">
        <!-- Toolbar -->
        <ToolBar @on_search_text_changed="onSearchTextChanged" />
        <div class="bottom-page-wrapper">
            <!-- Summary -->
            <div class="bottom">
                <!-- Summary Section -->
                <div class="summary">
                    <div v-for="filter in $store.getters['inventory/get_filters']" :key="filter.ref" class="tile-wrapper">
                        <SummaryTile
                            @click="setFilter(filter.value)"
                            :caption="filter.name"
                            :subtext="filter.subtext"
                            :count="filter.count" 
                            :theme="filter.theme"
                            :icon="filter.icon"
                            :selected="filter.value === this.filter"
                            v-on:on_search_text_changed="onSearchTextChanged"/>
                    </div>
                </div>
            </div>
            <!-- Inventory Overview -->
            <div class="inventory-overview-wrapper">
                <div class="top">
                    <div class="title">
                        Inventory Overview
                    </div>
                    <div class="filter">
                        <select v-model="filter">
                            <option value="*">All Stock</option>
                            <option value="in-stock">In Stock</option>
                            <option value="out-of-stock">Out of Stock</option>
                            <option value="low-stock">Low Stock</option>
                            <option value="expired">Expired</option>
                            <option value="almost-expired">Almost Expired</option>
                        </select>
                    </div>
                    <div class="add-product" @click="addProduct">
                        <div class="button-wrapper">
                            <PlainButton  
                                title="Add Item"
                                text="Add Item"/>
                        </div>
                    </div>
                </div>
                <div class="inventory-list-header">
                    <div class="item">
                        #
                    </div>
                    <div class="item">
                        Image
                    </div>
                    <div class="item">
                        Reference
                    </div>
                    <div class="item">
                        Name
                    </div>
                    <div class="item">
                        Description 
                    </div>
                    <div class="item">
                        Filter
                    </div>
                    <div class="item">
                        Price
                    </div>
                    <div class="item">
                        Sold
                    </div>
                    <div class="item">
                        Reorder
                    </div>
                    <div class="item">
                        Stock
                    </div>
                </div>
                <div class="inventory-list">
                    <div 
                        @click="editProduct(product.ref)"
                        v-for="(product,index) in filtered_inventory"  
                        :key="product.ref" 
                        class="inventory-item">
                        <div class="item">
                            <b>{{index + 1}}</b>
                        </div>
                        <div class="item">
                            <img :src="product.image_url" />
                        </div>
                        <div class="item">
                            <b>{{product.ref}}</b>
                        </div>
                        <div class="item">
                            {{product.name}}
                        </div>
                        <div class="item">
                            {{product.description}}
                        </div>
                        <div class="item">
                            In Stock
                        </div>
                        <div class="item">
                            ${{product.price_usd}}
                        </div>
                        <div class="item">
                            {{product.sold }}
                        </div>
                        <div class="item">
                            {{ product.reorder_point }}
                        </div>
                        <div class="item">
                            {{product.in_stock}}
                        </div>
                    </div>
                </div>
            </div>
            <!-- Space at the bottom -->
            <br>
            <br>
        </div>
    </div>
</template>

<style scoped>
    .inventory-wrapper {
        width: 100%;
        height: 100vh;
        overflow: hidden;
    }

    .bottom-page-wrapper {
        height: calc(100vh - 50px);
        overflow-y: scroll;
        overflow-x: hidden;
    }

    .summary{
        display: flex;
        column-gap: 10px;
        padding: 10px;
        width: calc(100vw - 50px);
        overflow-x: scroll;
    }
    
    .inventory-overview-wrapper {
        background-color: white;
        margin-left: 10px;
        margin-right: 10px;
        padding: 10px 10px;
        padding-bottom: none;
        border-radius: 8px;
        padding-bottom: 15px;
    } 

    .inventory-overview-wrapper .top {
        display: grid;
        grid-template-columns: auto 110px 70px;
        grid-column-gap: 10px;
    }

    .inventory-overview-wrapper .top .title {
        font-size: 0.9rem;
        margin-top: 8px;
    }

    select {
        height: 30px;
        border-radius: 5px;
        background-color: white;
        min-width: 100px;
        padding-left: 5px;
        padding-right: 5px;
        font-size: 0.7rem;
        border: solid rgb(203, 203, 203) 1px;
    }

    .inventory-list-header {
        margin-top: 15px;
        display: grid;
        grid-template-columns: 0.5fr 0.75fr 1.3fr 2.4fr 2.2fr 1.3fr 1.05fr 1fr 1fr 1fr;
        font-size: 0.8rem;
        background-color: #F5F5F5;
        height: 40px;
        padding-left: 15px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        border: solid 1.2px rgba(114, 114, 114, 0.067);
    }

    .inventory-list-header> div {
        display: flex;
        align-items: center;
        border-right: solid 1.2px rgba(114, 114, 114, 0.067);
        padding-left: 8px;
    }

    .inventory-item {
        display: grid;
        grid-template-columns: 0.5fr 0.75fr 1.3fr 2.4fr 2.2fr 1.3fr 1.05fr 1fr 1fr 1fr;
        font-size: 0.8rem;
        height: 40px;
        padding-left: 15px;
        background-color: white;
        border-bottom: solid 1.2px rgba(136, 136, 136, 0.067);
        cursor: pointer;
        transition: all 0.1s ease-in;
    }

    .inventory-item:hover{
        background-color: rgba(206, 206, 206, 0.271);
    }
    .inventory-item:last-child{
        border-bottom: none;
    }

    .inventory-item > div {
        display: flex;
        align-items: center;
        white-space: nowrap;       /* Prevents line break */
        overflow: hidden;          /* Hides overflow content */
        text-overflow: ellipsis; 
        padding-left: 8px;
    }
    
    .inventory-item  img {
        height: 25px;
        width: 25px;
        object-fit: cover;
    }

</style>

<script>
    import LeftIconedInput from '@/components/LeftIconedInput.vue';
    import ToolBar from '@/components/ToolBar.vue';
    import SummaryTile from '@/components/SummaryTile.vue';
    import PlainButton from '@/components/PlainButton.vue';
    
    export default {
        name : "InventoryTab",
        components: {
            LeftIconedInput,
            ToolBar,
            SummaryTile,
            PlainButton
        },
        data(){
            return {
                filter : "*",
                searchText: ""
            }
        },
        computed : {
            filtered_inventory(){
                
                let products = this.$store.getters["inventory/get_inventory"]

                products = products.filter(product => {
                    return (
                        product.name.toLowerCase().includes(this.searchText.toLowerCase()) ||
                        product.ref.toLowerCase().includes(this.searchText.toLowerCase())  ||
                        product.description.toLowerCase().includes(this.searchText.toLowerCase())
                    )
                })

                // All selected 
                if (this.filter === "*"){
                    return products  
                }

                // Apply filter 
                products = products.filter(item => {
                    
                    // Value to set
                    if (item.filter == null || item.filter.value === null){
                        return false
                    }

                    // Return the filter
                    return item.filter.value === this.filter
                })
                
                return products
            }
        },
        methods: {
            onSearchTextChanged(payload){
                this.searchText = payload
            },
            setFilter(filter){
                this.filter = filter
            },
            addProduct(){
                this.$router.push('add-product')
            },
            editProduct(ref){
                this.$router.push({
                    name: "edit-product",
                    params: { reference: ref }
                })
            }
        },
        mounted(){
            // Fetch inventory
            this.$store.dispatch("inventory/fetchInventory")
            // Get filters for inventory
            this.$store.dispatch('inventory/fetchFilters')
        }
    }
</script>