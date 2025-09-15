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
                        <TitledInput_v2
                            title="Product Reference"
                            :fill="true"
                            :editable="false"
                            placeholder="This feild is system generated"
                            v-model="payload.reference"/>
                        <div class="input-hint">This feild is auto generated and cannot be filled in.</div>
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledInput_v2
                            title="Product Name"
                            :fill="true"
                            placeholder="Product name i.e. Giesha Bathing Soap 200g"
                            v-model="payload.name"
                            :editable="submitted || processing"/>
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledInput_v2 
                            title="Product Description"
                            :fill="true"
                            :editable="submitted"
                            placeholder="Product description i.e Luxury bathing soap each"
                            v-model="payload.description"/>
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledSelect_v2
                            title="Product Category"
                            placeholder="Select the category"
                            :fill="true"
                            :editable="submitted || processing"
                            :options="category_options"
                            v-model="payload.category"/>
                        <div class="input-hint">Please select the most appropriate category for this item. This helps ensure that your product or service is correctly grouped and easily discoverable by users browsing or searching within the platform.</div>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput_v2 
                            title="Price USD"
                            :fill="true"
                            :editable="submitted || processing"
                            type="number"
                            placeholder="0"
                            validator="price"
                            v-model="payload.price_usd"/>
                        <div class="input-hint">Setting the ZWL price is not a reauirement after setting this value.</div>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput_v2
                            title="Price ZWL"
                            :fill="true"
                            :editable="submitted || processing"
                            placeholder="0"
                            type="none"
                            validator="price"
                            v-model="payload.price_zwg"/>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput_v2
                            title="Reorder Point"
                            :fill="true"
                            :editable="submitted || processing"
                            placeholder="0"
                            type="number"
                            validator="price"
                            v-model="payload.reorder_point"/>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput_v2
                            title="Expiry Buffer (Days)"
                            :fill="true"
                            :editable="submitted || processing"
                            placeholder="0"
                            type="number"
                            validator="price"
                            v-model="payload.expiry_day_buffer"/>
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
                        :editable="submitted || processing"
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
                            :disabled="processing"/>
                    </div>
                    <div style="margin-left:20px;" class="button-wrapper">
                        <PlainButton 
                            text="Create Product"
                            :loading="processing"
                            @on-click="createProduct"
                            theme="success"
                            :disabled="!submitted || !form_valid"/>
                    </div>
                </span>
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
        object-fit: contain;
    }

    .button-wrapper {
        margin-top: 15px;
        width: 100%;
    }
 </style>

<script>
    import ToolBar from '@/components/ToolBar.vue';
    import TitledInput from '@/components/TitledInput.vue';
    import TitledInput_v2 from '@/components/TitledInput_v2.vue';
    import { notify_failed, notify_success } from '@/utils/notifications';
    import TitledSelect from '@/components/TitledSelect.vue';
    import PlainButton from '@/components/PlainButton.vue';
    import { uploadFile } from '@/repo/FilesRepo';
    import { r_createProduct } from '@/repo/ProductsRepo';
    import error_mappings from '@/utils/error_mappings'
    import { r_getProduct } from '@/repo/ProductsRepo';
    import { backed_error_handler } from '@/utils/common';
    import TitledSelect_v2 from '@/components/TitledSelect_v2.vue';
    import { isNumberValid } from '@/utils/common';

    export default {
        name: "AddProductTab",
        components: {
            ToolBar,
            PlainButton,
            TitledInput_v2,
            TitledSelect_v2,
            TitledInput
        },
        data(){
            return {
                reference : "",
                product_categories: [],
                product_image: "/svg/images.svg",
                file : null,
                processing : false,
                payload: {
                    "image_upload" : null,
                    "category" : null,
                    "expiry_day_buffer" : null,
                    "price_usd" : 0,
                    "price_zwg" : 0,
                    "reference" : null,
                    "name" : null,
                    "description" : null,
                    "reorder_point" : null
                }
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
            submitted(){
                return this.payload.reference === null
            },
            form_valid() {
                return (
                    this.payload.category !== null &&
                    isNumberValid(this.payload.expiry_day_buffer) &&
                    isNumberValid(this.payload.price_usd, false) && // must be > 0
                    isNumberValid(this.payload.price_zwg) &&
                    this.payload.description !== null &&
                    this.payload.description.length > 3 &&
                    this.payload.name !== null &&
                    this.payload.name.length > 3 &&
                    isNumberValid(this.payload.reorder_point) &&
                    this.file !== null
                )
            }
        },
        methods: {
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
            onProductCreated(success,payload){
                // Stop processing 
                this.processing = false
                
                // Response 
                if (!success){
                    return backed_error_handler(payload)
                }

                // Set the reference
                this.payload.reference = payload.product.ref

                notify_success(`Product Created - ${this.payload.reference}`)

                // Redirect to edit product 
                this.$router.replace({ name: 'edit-product', params: { reference: this.payload.reference } })
            },
            onFileUploadResult(success,payload){
                // Not successful 
                if (success === false){
                    this.processing = false
                    return notify_failed(payload)
                }

                // Set the data as the image upload data
                this.payload.image_upload = payload.ref
                
                // Create the product
                r_createProduct(this.payload,this.onProductCreated)
                
            },
            createProduct(){
                // Start loading 
                this.processing = true

                // Upload a file first and then commit data 
                if (this.file){
                    // Upload image is it hasnt
                    if (!this.payload.image_upload){
                        return uploadFile(this.file,this.onFileUploadResult)
                    }

                    // Create the product - image has already been upload
                    r_createProduct({
                        ...this.payload,
                        price_zwg: [null, "",NaN].includes(this.payload.price_zwg) ? 0 : this.payload.price_zwg,
                        reorder_point: [null, "",NaN].includes(this.payload.reorder_point) ? 0 : this.payload.reorder_point,
                        expiry_day_buffer: [null, "",NaN].includes(this.payload.expiry_day_buffer) ? 0 : this.payload.expiry_day_buffer
                    },this.onProductCreated)
                }
            },
            // When the duplicate product is returned 
            onDuplicateProductResult(success,payload){
                // Handle failure 
                if (!success){
                    return backed_error_handler(payload)
                }
                
                // Success then set the params
                const product = payload.product

                if (product){
                    this.payload = {
                        ...this.payload,
                        category : product.category.ref,
                        expiry_day_buffer: product.expiry_day_buffer,
                        price_usd: product.price_usd,
                        price_zwg: 0,
                        name: product.name,
                        description: product.description,
                        reorder_point: product.reorder_point
                    }
                }
            },
            init(){
                // If there is a reference then copy over the data for that product to the current context
                if (this.$route.params.reference){
                    // Fetch the product 
                    const duplicateProductReference = this.$route.params.reference
                    // Get the product from the database 
                    r_getProduct(this.onDuplicateProductResult,duplicateProductReference)
                }
            }
        },  
        mounted(){
            this.init()
        }
    }
</script>