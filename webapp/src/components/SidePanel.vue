<template>  
    <div class="side-panel-wrapper">
        <div class="title-wrapper">
            Invoice
        </div>
        <div class="products-list">
            <div class="product-wrapper">
                <ProductSmall />
            </div>
            <div class="product-wrapper">
                <ProductSmall />
            </div>
            <div class="product-wrapper">
                <ProductSmall />
            </div>
            <div class="product-wrapper">
                <ProductSmall />
            </div>
            <div class="product-wrapper">
                <ProductSmall />
            </div>
            <div class="product-wrapper">
                <ProductSmall />
            </div>
            <div class="product-wrapper">
                <ProductSmall />
            </div>
        </div>
        <div class="payment-summary">
            <div class="title">
                Payment Summary
            </div>
            <div class="summary">
                <div>Sub Total</div>
                <div style="margin-left: auto;">$<b>131.2</b></div>
                <div>Tax</div>
                <div style="margin-left: auto;">$<b>5.2</b></div>
            </div>
            <div class="dotted-line"></div>
            <div class="summary">
                <div>Total Payment</div>
                <div style="margin-left: auto;">$<b>136.4</b></div>
            </div>
            <div class="payment-types-wrapper">
                <div class="payment-type" 
                    :class="{selected : payment_type === 'swipe'}"
                    @click="changePaymentType('swipe')">
                    <div class="payment-icon-wrapper">
                        <img src="/svg/credit-card.svg" alt="" class="payment-icon">
                    </div>
                    <div class="bottom">
                        Swipe
                    </div>
                </div>
                <div class="payment-type" 
                    :class="{selected : payment_type === 'cash'}"
                    @click="changePaymentType('cash')">
                    <div class="payment-icon-wrapper">
                        <img src="/svg/money-bills.svg" alt="" class="payment-icon">
                    </div>
                    <div class="bottom">
                        Cash
                    </div>
                </div>
                <div class="payment-type" 
                    :class="{selected : payment_type === 'ecocash'}"
                    @click="changePaymentType('ecocash')">
                    <div class="payment-icon-wrapper">
                        <img src="/svg/money-bills.svg" alt="" class="payment-icon">
                    </div>
                    <div class="bottom">
                        EcoCash
                    </div>
                </div>
            </div>
        </div>
        <div class="finish-button">
            <PlainButton text="Complete Cart" theme="orange"/>
        </div>
    </div>
</template>

<style lang="css" scoped>
    .side-panel-wrapper {
        background-color: white;
        border: solid 1.8px rgba(128, 128, 128, 0.203);
        border-radius: 8px;
        height: calc(100vh - 100px);
        position: relative;
    }

    .side-panel-wrapper .title-wrapper {
        margin-left: 15px;
        margin-top: 15px;
        font-size: 1.2rem;
        font-weight: bold;
        color: rgb(86, 86, 86);
    }

    .side-panel-wrapper .products-list {
        margin-left: 15px;
        margin-top: 15px;
        height: 40%;
        overflow-y: scroll;
    }

    .side-panel-wrapper .products-list::-webkit-scrollbar{
        display: none;
    }

    .product-wrapper {
        margin-top: 15px;
    }

    .payment-summary {
        background-color: #FAFAFA;
        margin-left: 15px;
        margin-right: 15px;
        margin-top: 15px;
        padding-top: 10px;
        padding-bottom: 10px;
        border-radius: 5px;
        color: rgb(83, 83, 83);
    }

    .payment-summary .title {
        font-size: 0.95rem;
        font-weight: bold;
        margin-left: 10px;
    }

    .payment-summary .summary {
        display: grid;
        grid-template-columns: 1fr 1fr;
        margin-left: 10px;
        margin-right: 10px;
        font-size: 0.85rem;
        margin-top: 15px;
        grid-row-gap: 8px;
    }

    .dotted-line {
        border: 0px;
        border-bottom: solid 1.2px rgb(44, 44, 44);
        height: 1.2px;
        border-style: dashed;
        display: flex;
        width: calc(100% - 20px);
        margin-top: 10px;
        margin-left: auto;
        margin-right: auto;
    }

    .payment-types-wrapper {
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
        padding: 4px;
        margin-top: 15px;
        border-radius: 8px;
        background-color: #F2F1F2;
    }

    .payment-type{
        width: 90px;
        height: fit-content;
        font-size: 0.7rem;
        color: grey;
        border-radius: 5px;
        padding-top: 5px;
        padding-bottom: 5px;
        transition: all 0.1s ease-in;
    }

    .payment-type.selected {
        background-color: white;
        color: rgba(243, 138, 27, 0.86);
        font-weight: bold;
    }

    .payment-type > div {
        display: flex;
        justify-content: center;
    }

    .payment-type .bottom {
        margin-top: 2px;
    }

    .payment-types-wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        cursor: pointer;
    }

    .payment-icon-wrapper {
        width: fit-content;
        height: fit-content;
        margin-left: auto;
        margin-right: auto;
        padding: 5px;
    }

    .payment-icon-wrapper{
        opacity: 0.7;
    }

    .payment-icon-wrapper img {
        height: 15px;
        width: 15px;
    }

    .finish-button {
        position: absolute;
        margin: 15px;
        margin-bottom: 0;
        bottom: 10px;
        left: 0px;
        width: calc(100% - 30px);
    }
</style>

<script>
    import ProductSmall from './ProductSmall.vue';
    import PlainButton from './PlainButton.vue';
    
    export default {
        name : 'SidePanel',
        components: {
            ProductSmall,
            PlainButton
        },
        data(){
            return {
                payment_type: "swipe"
            }
        },
        methods: {
            changePaymentType(newType){
                this.$data.payment_type = newType
            }
        }
    }
</script>