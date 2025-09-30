<template>
    <div class="add-product-wrapper">
        <ToolBar />
        <div class="bottom-wrapper">
            <div class="left">
                <div class="title">
                    Add Product 
                </div>
                <div class="title">
                    <span class="link-top-right inline" @click="duplicateProduct">Duplicate Product</span>
                    <span style="margin-left: 10px;" class="link-top-right" @click="toogleAddStockWindow(true)">Add Stock</span>
                </div>
                <div class="grid-two">
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledInput_v2
                            title="Product Reference"
                            :fill="true"
                            :editable="false"
                            placeholder="This feild is system generated"
                            v-model="product.ref"/>
                        <div class="input-hint">This feild is auto generated and cannot be filled in.</div>
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledInput_v2
                            title="Product Name"
                            :fill="true"
                            placeholder="Product name i.e. Giesha Bathing Soap 200g"
                            v-model="product.name"
                            :editable="!processing" />
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledInput_v2
                            title="Product Description"
                            :fill="true"
                            :editable="!processing"
                            placeholder="Product description i.e Luxury bathing soap each"
                            v-model="product.description"/>
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledSelect_v2
                            title="Product Category"
                            placeholder="Select the category"
                            :fill="true"
                            :editable="!processing"
                            :options="category_options"
                            v-model="product.category"/>
                        <div class="input-hint">Please select the most appropriate category for this item. This helps ensure that your product or service is correctly grouped and easily discoverable by users browsing or searching within the platform.</div>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput_v2
                            title="Price USD"
                            :fill="true"
                            :editable="!processing"
                            type="number"
                            placeholder="0"
                            validator="price"
                            v-model="product.price_usd"/>
                        <div class="input-hint">Setting the ZWL price is not a reauirement after setting this value.</div>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput_v2
                            title="Price ZWL"
                            :fill="true"
                            :editable="!processing"
                            placeholder="0"
                            type="number"
                            validator="none"
                            v-model="product.price_zwg"/>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput_v2
                            title="Reorder Point"
                            :fill="true"
                            :editable="!processing"
                            placeholder="0"
                            type="number"
                            validator="price"
                            v-model="product.reorder_point"/>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput_v2
                            title="Expiry Buffer (Days)"
                            :fill="true"
                            :editable="!processing"
                            placeholder="0"
                            type="number"
                            validator="price"
                            v-model="product.expiry_day_buffer"/>
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
                        :editable="!processing"
                        :value="reference"
                        type="file"
                        @on-change="onFileChange"/>

                    <div class="input-hint">Upload a clear and high-quality image of the product. This image will be displayed on the product listing and should accurately represent what you're offering.</div>
                </div>
                <!-- Button to make the submition  -->
                <span style="display:flex;">
                    <div class="button-wrapper">
                        <PlainButton 
                            text="Cancel"
                            theme="warn"
                            @on-click="$router.back()"
                            :disabled="processing || add_stock_submitting"/>
                    </div>
                    <div style="margin-left:20px;" class="button-wrapper">
                        <PlainButton 
                            text="Save Changes"
                            :loading="processing"
                            @on-click="updateProduct"
                            theme="success"
                            :disabled="!form_valid || add_stock_submitting"/>
                    </div>
                </span>
            </div>
        </div>
        
        <!-- Additional Components -->
        <PopupForm 
            :product_reference="product.ref"
            v-if="showAddStockWindow" 
            @close-window="toogleAddStockWindow(false)"
            @submitting="addStockFormSubmitting" />
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
        margin-top: 5px;
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
        object-fit: contain;
    }

    .button-wrapper {
        margin-top: 15px;
        width: 100%;
    }

    
    .link-top-right {
        font-size: 0.7rem;
        color: #4d99f7;
        cursor: pointer;
        margin-left: 5px;
    }

    .link-top-right:hover{
        color: #2a5385;
        text-decoration: underline;
    }

    .link-top-right.inline {
        margin-left: 0px;
        margin-top: 15px;
    }
 </style>

<script>
    import ToolBar from '@/components/ToolBar.vue';
    import TitledInput from '@/components/TitledInput.vue';
    import { notify_failed, notify_success } from '@/utils/notifications';
    import PlainButton from '@/components/PlainButton.vue';
    import { uploadFile } from '@/repo/FilesRepo';
    import { r_updateProduct, r_getProduct } from '@/repo/ProductsRepo';
    import { backed_error_handler } from '@/utils/common';
    import TitledInput_v2 from '@/components/TitledInput_v2.vue';
    import TitledSelect_v2 from '@/components/TitledSelect_v2.vue';
    import PopupForm from '@/components/PopupForm.vue';

    export default {
        name: "EditProductTab",
        components: {
            ToolBar,
            TitledSelect_v2,
            PlainButton,
            TitledInput_v2,
            TitledInput,
            PopupForm
        },
        data(){
            return {
                reference : "",
                product_categories: [],
                product_image: "/svg/images.svg",
                file : null,
                processing : false,
                add_stock_submitting: false,
                product: {
                    "image_upload" : null,
                    "category" : "",
                    "expiry_day_buffer" : 0,
                    "price_usd" : 0,
                    "price_zwg" : 0,
                    "ref" : "",
                    "name" : "",
                    "description" : "",
                    "reorder_point" : 0
                },
                showAddStockWindow : false
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
            },
            form_valid(){
                return (
                    this.product.category !== null &&
                    this.product.expiry_day_buffer !== null &&
                    this.product.price_usd !== null &&
                    this.product.price_usd > 0 &&
                    this.product.description !== null &&
                    this.product.description.length > 3 &&
                    this.product.name !== null &&
                    this.product.name.length > 3 &&
                    this.product.reorder_point !== null
                )
            }
        },
        methods: {
            // Get the product from the backend 
            init(){
                // Get the product 
                let productReference = this.$route.params.reference
                r_getProduct(this.onGetProductResult,productReference)
            },
            // When the product result is returned
            onGetProductResult(success,payload){
                
                // Failed
                if (success == false){
                    return backed_error_handler(payload)
                }

                // Success then set the product as the one from the response 
                if (payload.product){
                    // Product
                    const product = payload.product

                    // Map the response to that of the ui
                    this.product = {
                        ...this.product,
                        category: product.category.ref,
                        expiry_day_buffer: product.expiry_day_buffer,
                        price_usd: product.price_usd,
                        price_zwg: 0,
                        ref: product.ref,
                        name: product.name,
                        description: product.description,
                        reorder_point: product.reorder_point
                    }

                    // Set the existing image 
                    this.product_image = product.image_url
                    return
                }
                
                notify_failed('Failed to process response from server')
            },
            onFileChange(event){
                const selectedFile = event.target.files[0]

                if (selectedFile){
                    this.file = selectedFile

                    // Generate the preview url
                    const reader = new FileReader();
                    reader.readAsDataURL(this.file);
                    reader.onload = () => {
                        this.product_image = reader.result;
                    };
                }
            },
            onProductUpdateResult(success,payload){

                // Stop processing 
                this.processing = false
                
                // Handle error 
                if (success === false){
                    return backed_error_handler(payload)
                }

                const updated = payload.product.after

                // Map backend response → UI product
                this.product = {
                    ...this.product, // keep previous local fields like image_upload
                    category: updated.category.ref,
                    expiry_day_buffer: updated.expiry_day_buffer,
                    price_usd: updated.price_usd,
                    price_zwg: updated.price_zwg || 0,
                    ref: updated.ref,
                    name: updated.name,
                    description: updated.description,
                    reorder_point: updated.reorder_point,
                    image_upload: null
                }

                // Update image if included
                if (updated.image_url) {
                    this.product_image = updated.image_url
                }

                // Remove the file to prevent another upload 
                this.file = null

                // Notify the success
                notify_success(`Product Updated - ${this.product.ref}`)
            },
            onFileUploadResult(success,payload){                
                // Not successful 
                if (success === false){
                    return backed_error_handler(payload)
                }

                // Set the data as the image upload data
                this.product.image_upload = payload.ref
                
                // Create the product
                r_updateProduct(this.product,this.product.ref,this.onProductUpdateResult)
                
            },
            updateProduct(){
                // Start loading 
                this.processing = true

                // Upload image if it is there
                if (this.file){
                    return uploadFile(this.file,this.onFileUploadResult)
                }

                // Create the product - image has already been upload
                r_updateProduct(this.product,this.product.ref,this.onProductUpdateResult)
            },
            toogleAddStockWindow(show){
                this.showAddStockWindow = show
            },
            addStockFormSubmitting(state){
                this.add_stock_submitting = state
            },
            // Call create product with a duplicate option
            duplicateProduct(){
                this.$router.push({name: "add-product",params: { reference : this.product.ref}})
            }
        },
        mounted(){
            // Initialize
            this.init()
        }
    }
</script>