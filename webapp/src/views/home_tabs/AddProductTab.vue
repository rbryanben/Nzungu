<template>
    <div class="add-product-wrapper">
        <ToolBar />
        <div class="bottom-wrapper">
            <div class="left">
                <div class="title">
                    Add Product
                </div>
                <div class="grid-two">
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledInput 
                            title="Product Reference"
                            :fill="true"
                            :editable="false"
                            ref="product_reference_titled_input"/>

                        <div class="input-hint">This feild is auto generated and cannot be filled in.</div>
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledInput 
                            title="Product Name"
                            :fill="true"
                            placeholder="Product name i.e. Giesha Bathing Soap 200g"/>
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledInput 
                            title="Product Description"
                            :fill="true"
                            placeholder="Product description i.e Luxury bathing soap each"/>
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledSelect
                            title="Product Category"
                            placeholder="Select the category"
                            :fill="true"
                            :options="category_options"/>
                        <div class="input-hint">Please select the most appropriate category for this item. This helps ensure that your product or service is correctly grouped and easily discoverable by users browsing or searching within the platform.</div>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput 
                            title="Price USD"
                            :fill="true"
                            type="number"
                            placeholder="0"
                            validator="price"/>
                        <div class="input-hint">Setting the ZWL price is not a reauirement after setting this value.</div>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput 
                            title="Price ZWL"
                            :fill="true"
                            placeholder="0"
                            type="number"
                            validator="price"/>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput 
                            title="Reorder Point"
                            :fill="true"
                            placeholder="0"
                            type="number"
                            validator="price"/>
                    </div>
                </div>
            </div>
            <div class="right">
                <div class="title">
                    Add Images
                </div>
                <div class="image-preview">
                    <img :src="product_image" alt="" class="product-image-preview">
                </div>
                <div class="input-wrapper" style="grid-column: span 2;">
                    <TitledInput 
                        title="Select Image"
                        :fill="true"
                        :value="reference"
                        type="file"/>

                    <div class="input-hint">Upload a clear and high-quality image of the product. This image will be displayed on the product listing and should accurately represent what you're offering.</div>
                </div>
                <!-- Button to make the submition  -->
                <div class="button-wrapper">
                    <PlainButton 
                        text="Create Product"/>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .bottom-wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
    }

    .left,.right {
        margin: 15px;
        padding: 15px;
        background-color: white;
        border-radius: 8px;
        height: calc(100vh - 130px);
        overflow-y: scroll;
    }

    .title {
        font-weight: bold;
        font-size: 1.2rem;
    }

    .input-wrapper{
        margin-top: 10px;
    }

    .grid-two {
        margin-top: 15px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-column-gap: 20px;
    }

    .input-hint {
        margin-top: 9px;
        margin-bottom: 10px;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .image-preview {
        border: dashed 1.2px grey;
        height: 250px;
        width: 100%;
        margin-left: auto;
        margin-right: auto;
        margin-top: 10px;
        border-radius: 5px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .image-preview img {
        height: 180px;
        width: 220px;
    }

    .button-wrapper {
        margin-top: 15px;
        width: 250px;
    }
 </style>

<script>
    import ToolBar from '@/components/ToolBar.vue';
    import TitledInput from '@/components/TitledInput.vue';
    import { generateReference } from '@/repo/ProductsRepo';
    import { notify_failed } from '@/utils/notifications';
    import TitledSelect from '@/components/TitledSelect.vue';
    import PlainButton from '@/components/PlainButton.vue';

    export default {
        name: "AddProductTab",
        components: {
            ToolBar,
            TitledInput,
            TitledSelect,
            PlainButton
        },
        data(){
            return {
                reference : "",
                product_categories: [],
                product_image: "/svg/images.svg"
            }
        },
        computed: {
            category_options(){
                let categories = this.$store.state.sales.categories
                return categories.filter(category => category.ref !== "*").map(category => {
                    return {
                        "name" : category.name,
                        "ref" : category.ref
                    }
                })
            }
        },
        methods: {
            onReferenceReceived(success,payload){
                // Alert the generation failure
                if (!success){
                    notify_failed(payload)
                    return
                }

                this.$refs.product_reference_titled_input.setText(payload.reference)
            }
        },  
        mounted(){
            // Fetch a unique reference
            generateReference(this.onReferenceReceived)
        }
    }
</script>