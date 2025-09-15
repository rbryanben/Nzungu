<template>
    <div class="form-wrapper">
        <div class="title">Add Stock</div>

        <!-- Inputs -->
        <div style="margin-top: 30px;" class="input-wrapper">
            <TitledInput_v2
                title="Product Reference"
                :fill="true"
                validator="none"
                :editable="false"
                v-bind:model-value="product_reference"
                placeholder="This feild is system generated"/>
            <div class="input-hint">This feild is auto generated and cannot be filled in.</div>
        </div>
        <div class="input-wrapper">
            <TitledInput_v2
                title="Earliest Expiry Date"
                :fill="true"
                validator="none"
                type="date"
                v-model="stock_payload.earlist_expiry_date"
                placeholder="This feild is system generated"/>
            <div class="input-hint">Select the earliest expiry date</div>
        </div>
        <div class="input-wrapper">
            <TitledInput_v2
                title="Count in Units"
                :fill="true"
                validator="number"
                :placeholder="0"
                v-model="stock_payload.stock_count"
                type="number"/>
        </div>
        <div class="input-wrapper">
            <TitledInput_v2
                title="Buying Price Each (USD)"
                :fill="true"
                validator="none"
                v-model="stock_payload.buying_price_usd_each"
                :placeholder="0"
                type="number"/>
        </div>
        <div class="input-wrapper">
            <TitledInput_v2
                title="Buying Price Each (ZWG)"
                :fill="true"
                validator="none"
                v-model="stock_payload.buying_price_zwg_each"
                :placeholder="0"
                type="number"/>
        </div>
        <div class="buttons-wrapper">
            <div class="button-wrapper">
                <PlainButton 
                    title="Cancel"
                    text="Cancel"
                    theme="orange"
                    @click="$emit('close-window')"
                    :disabled="submitting"/>
            </div>
            <div class="button-wrapper">
                <PlainButton 
                    title="Add Stock"
                    text="Add Stock"
                    theme="green"
                    :loading="submitting"
                    @click="addStock"
                    :disabled="!form_valid"/>
            </div>
        </div>
    </div>
</template>

<style scoped>

    .form-wrapper {
        background-color: white;
        border-radius: 5px;
        position: fixed;
        top: 50%;
        left: 50%;
        width: 400px;
        padding: 20px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 
                    0 6px 20px 0 rgba(0, 0, 0, 0.19);
        transform: translate(-50%, -50%) scale(0.7);
        opacity: 0;
        animation: zoomIn 0.1s ease-out forwards;
    }

    @keyframes zoomIn {
        0% {
            transform: translate(-50%, -50%) scale(0.7);
            opacity: 0;
        }
        100% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 1;
        }
    }

    .input-wrapper {
        margin-top: 15px;
    }

    .title {
        font-weight: bold;
        font-size: 1.2rem;
    }

    .buttons-wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        margin-top: 30px;
        grid-column-gap: 10px;
    }

    .input-hint {
        margin-top: 9px;
        margin-bottom: 10px;
        font-size: 0.8rem;
        opacity: 0.7;
    }
</style>

<script>
    import TitledInput_v2 from './TitledInput_v2.vue';
    import TitledInput from './TitledInput.vue';
    import PlainButton from './PlainButton.vue';
    import { r_addStock } from '@/repo/ProductsRepo';
    import { backed_error_handler } from '@/utils/common';
    import { notify_success } from '@/utils/notifications';
    import validators from '@/shared/validators';
    
    export default {
        name: 'PopupForm',
        components: {
            TitledInput_v2,
            PlainButton,
            TitledInput
        },
        data(){
            return {
                stock_payload : {
                    earlist_expiry_date: new Date().toISOString().split("T")[0],
                    stock_count : 0,
                    buying_price_usd_each : 0,
                    buying_price_zwg_each : 0
                },
                submitting: false
            }
        },
        computed: {
            form_valid(){
                return validators.number(this.stock_payload.stock_count) && this.stock_payload.stock_count != 0
            }
        },
        methods: {
            clearValues(){
                this.stock_payload = {
                    ...this.stock_payload,
                    stock_count: 0, 
                    buying_price_usd_each: 0,
                    buying_price_zwg_each: 0
                }
            },
            setSubmitting(state){
                this.submitting = state
                this.$emit('submitting',this.submitting)
            },
            onAddStockResult(success,payload){
                // Stop loading 
                this.setSubmitting(false)

                // Was not successful 
                if (!success){
                    return backed_error_handler(payload)
                }

                // Success show notiication
                notify_success(`Added ${this.stock_payload.stock_count} items to stock`)

                // Clear values 
                this.clearValues()

                // Notify close 
                this.$emit('close-window')

            },
            addStock(){
                // Start loading 
                this.setSubmitting(true)

                // Send the request to submit 
                r_addStock({
                    ...this.stock_payload,
                    "product_reference" : this.product_reference
                },this.onAddStockResult)
            }
        },
        props: {
            product_reference: {
                type: String,
                default: "some-product-reference"
            }
        }
    }
</script>