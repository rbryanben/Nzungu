<template>
    <div class="inventory-wrapper">
        <!-- Toolbar -->
        <ToolBar @on_search_text_changed="onSearchTextChanged" @refresh-page="init()" />

        <div class="bottom-page-wrapper">
            <!-- Summary Wrapper -->
            <div class="summary-wrapper">
                <div class="summary-item">
                    <CurrencyValueTile
                        currency="USD"
                        :amount="total_cash_usd" />
                </div>
                <div class="summary-item">
                    <CurrencyValueTile
                        currency="ZWG"
                        :amount="total_cash_zwg" />
                </div>
                <div class="summary-item">
                    <CurrencyValueTile
                        currency="USD"
                        title="Total Bank"
                        :amount="total_bank_usd" />
                </div>
                <div class="summary-item">
                    <CurrencyValueTile
                        currency="ZWG"
                        title="Total Bank"
                        :amount="total_bank_zwg" />
                </div>
            </div>
            <!-- Inventory Overview -->
            <div class="inventory-overview-wrapper">
                <div class="top">
                    <div class="title">
                        Daily Sales
                    </div>
                    <div class="filter">
                        <select v-model="period" @change="init">
                            <option value="day">Today's Sales</option>
                            <option value="two-days">Yesterdays Sales</option>
                            <option value="week">Weekly Sales</option>
                            <option value="month">Monthly Sales</option>
                        </select>
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
                        Name
                    </div>
                    <div class="item">
                        Description 
                    </div>
                    <div class="item">
                        Count
                    </div>
                    <div class="item">
                        PayMethod
                    </div>
                    <div class="item">
                        Currency
                    </div>
                    <div class="item">
                        Unit Price
                    </div>
                    <div class="item">
                        Total Price
                    </div>
                </div>
                <div class="inventory-list">
                    <span
                        v-for="cart in carts"
                        :key="cart.ref">
                        <div class="group-sale">
                            {{isoToHumanReadable(cart.timestamp)}}
                        </div>
                        <div v-for="(product,index) in cart.items" :key="cart.ref + product.ref" class="inventory-item">
                            <div class="item">
                                <b>{{index}}</b>
                            </div>
                            <div class="item">
                                <img :src="product.image_url" />
                            </div>
                            <div class="item">
                                {{product.name}}
                            </div>
                            <div class="item">
                                {{product.description}}
                            </div>
                            <div class="item">
                                x{{product.count}}
                            </div>
                            <div class="item">
                                {{cart.payment_method}}
                            </div>
                            <div class="item">
                                {{cart.currency}}
                            </div>
                            <div class="item">
                                ${{cart.currency === 'USD' ? formatTwoDecimals(product.price_usd) : formatTwoDecimals(product.price_zwg) }}
                            </div>
                            <div class="item">
                                ${{cart.currency === 'USD' ?  formatTwoDecimals(product.price_usd * product.count) : formatTwoDecimals(product.price_zwg * product.count)}}
                            </div>
                        </div>
                    </span>
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
        margin-top: 5px;
    }

    .summary-wrapper {
        display: flex;
        column-gap: 10px;
        padding: 10px;
        width: calc(100vw - 50px);
        overflow-x: scroll;
    }

    .group-sale {
        margin-left: 20px;
        margin-top: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        margin-bottom: 10px;
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
        grid-template-columns: auto 100px 50px;
        grid-column-gap: 10px;
    }

    .inventory-overview-wrapper .top .title {
        font-size: 1.2rem;
        margin-top: 8px;
    }

    select {
        height: 40px;
        border-radius: 5px;
        background-color: white;
        min-width: 90px;
        padding-left: 5px;
        padding-right: 5px;
        font-size: 0.9rem;
        border: solid rgb(203, 203, 203) 1px;
    }

    .inventory-list-header {
        margin-top: 15px;
        display: grid;
        grid-template-columns: 0.5fr 0.75fr 2.9fr 2.2fr 1fr 1.05fr 1.05fr 1fr 1fr;
        font-size: 0.9rem;
        background-color: #F5F5F5;
        height: 40px;
        padding-left: 40px;
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
        grid-template-columns: 0.5fr 0.75fr 2.9fr 2.2fr 1fr 1.05fr 1.05fr 1fr 1fr;
        font-size: 0.9rem;
        height: 50px;
        padding-left: 40px;
        background-color: white;
        border-bottom: solid 1.2px rgba(136, 136, 136, 0.179);
        cursor: pointer;
        transition: all 0.1s ease-in;
    }

    .inventory-item .item {
        margin-top: auto;
        margin-bottom: auto;
        display: block;   
        width: 90%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
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
        height: 30px;
        width: 30px;
        object-fit: contain;
    }

    @media only screen and (max-width: 1200px) { 
    
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
            grid-template-columns: auto 110px 5px;
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
            grid-template-columns: 0.5fr 0.75fr 3.4fr 2.2fr 0.8fr 1.05fr 1.05fr 1fr 1fr;
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
            grid-template-columns: 0.5fr 0.75fr 3.4fr 2.2fr 0.8fr 1.05fr 1.05fr 1fr 1fr;
            font-size: 0.8rem;
            height: 40px;
            padding-left: 15px;
            background-color: white;
            border-bottom: solid 1.2px rgba(136, 136, 136, 0.204);
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
            height: 30px;
            width: 30px;
            object-fit: contain;
        }
}

</style>

<script>
    import LeftIconedInput from '@/components/LeftIconedInput.vue';
    import ToolBar from '@/components/ToolBar.vue';
    import SummaryTile from '@/components/SummaryTile.vue';
    import PlainButton from '@/components/PlainButton.vue';
    import { formatTwoDecimals, isoToHumanReadable } from '@/utils/common';
    import { getTellerSales } from '@/repo/SaleRepo';
    import { notify_failed } from '@/utils/notifications';
    import CurrencyValueTile from '@/components/CurrencyValueTile.vue';
    
    export default {
        name : "ViewSalesTab",
        components: {
            LeftIconedInput,
            ToolBar,
            SummaryTile,
            PlainButton,
            CurrencyValueTile
        },
        data(){
            return {
                searchText: "",
                period: "day",
                carts: [],
                sales: null
            }
        },
        computed: {
            total_cash_usd(){
                return this.sales && this.sales.cash_usd ? this.sales.cash_usd.total: 0
            },
            total_cash_zwg(){
                return this.sales && this.sales.cash_zwg ? this.sales.cash_zwg.total : 0
            },
            total_bank_usd(){
                return this.sales && this.sales.bank_usd ? this.sales.bank_usd.total : 0
            },
            total_bank_zwg(){
                return this.sales && this.sales.bank_zwg ? this.sales.bank_zwg.total : 0
            }
        },
        methods: {
            // Initialization method
            init(){
                // Get the sales by a teller
                getTellerSales(this.period,this.onTellerSalesResult)
            },
            // When search text changes handler set the search text as that
            onSearchTextChanged(payload){
                this.searchText = payload
            },
            // Callback when teller sales are received
            onTellerSalesResult(success,payload){
                // Failed request
                if (!success){
                    notify_failed(payload)
                    return
                }

                // Success then set the cart
                this.carts = payload.carts
                this.sales = payload.sales
            },
            // Method to format an amount to two decimal paces
            formatTwoDecimals: formatTwoDecimals,
            isoToHumanReadable: isoToHumanReadable       
        },
        mounted(){
            // Fetch teller sales
            this.init()
        }
    }
</script>