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
                            placeholder="This feild is system generated"
                            ref="reference_feild"/>
                        <div class="input-hint">This feild is auto generated and cannot be filled in.</div>
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledInput 
                            title="Product Name"
                            :fill="true"
                            placeholder="Product name i.e. Giesha Bathing Soap 200g"
                            @on-text-changed="e => payload.name = e"
                            :editable="submitted || processing"/>
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledInput 
                            title="Product Description"
                            :fill="true"
                            :editable="submitted"
                            placeholder="Product description i.e Luxury bathing soap each"
                            @on-text-changed="e => payload.description = e"/>
                    </div>
                    <div class="input-wrapper" style="grid-column: span 2;">
                        <TitledSelect
                            title="Product Category"
                            placeholder="Select the category"
                            :fill="true"
                            :editable="submitted || processing"
                            :options="category_options"
                            @on-text-changed="e => payload.category = e"/>
                        <div class="input-hint">Please select the most appropriate category for this item. This helps ensure that your product or service is correctly grouped and easily discoverable by users browsing or searching within the platform.</div>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput 
                            title="Price USD"
                            :fill="true"
                            :editable="submitted || processing"
                            type="number"
                            placeholder="0"
                            validator="price"
                            @on-text-changed="e => payload.price_usd = e"/>
                        <div class="input-hint">Setting the ZWL price is not a reauirement after setting this value.</div>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput 
                            title="Price ZWL"
                            :fill="true"
                            :editable="submitted || processing"
                            placeholder="0"
                            type="number"
                            validator="price"
                            @on-text-changed="e => payload.price_zwg = e"/>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput 
                            title="Reorder Point"
                            :fill="true"
                            :editable="submitted || processing"
                            placeholder="0"
                            type="number"
                            validator="price"
                            @on-text-changed="e => payload.reorder_point = e"/>
                    </div>
                    <div class="input-wrapper">
                        <TitledInput 
                            title="Expiry Buffer (Days)"
                            :fill="true"
                            :editable="submitted || processing"
                            placeholder="0"
                            type="number"
                            validator="price"
                            @on-text-changed="e => payload.expiry_day_buffer = e"/>
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
        width: 250px;
    }
 </style>

<script>
    import ToolBar from '@/components/ToolBar.vue';
    import TitledInput from '@/components/TitledInput.vue';
    import { notify_failed, notify_success } from '@/utils/notifications';
    import TitledSelect from '@/components/TitledSelect.vue';
    import PlainButton from '@/components/PlainButton.vue';
    import { uploadFile } from '@/repo/FilesRepo';
    import { r_createProduct } from '@/repo/ProductsRepo';
import router from '@/router';

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
                product_image: "/svg/images.svg",
                file : null,
                processing : false,
                payload: {
                    "image_upload" : null,
                    "category" : null,
                    "expiry_day_buffer" : 0,
                    "price_usd" : 0,
                    "price_zwg" : 0,
                    "reference" : null,
                    "name" : null,
                    "description" : null,
                    "reorder_point" : 0
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
            form_valid(){
                return (
                    this.payload.category !== null &&
                    this.payload.expiry_day_buffer !== null &&
                    this.payload.price_usd !== null &&
                    this.payload.price_usd > 0 &&
                    this.payload.description !== null &&
                    this.payload.description.length > 3 &&
                    this.payload.name !== null &&
                    this.payload.name.length > 3 &&
                    this.payload.reorder_point !== null &&
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
                
                // Set the reference
                this.payload.reference = payload.product.ref

                // Set in the UI
                this.$refs.reference_feild.setText(this.payload.reference)

                notify_success(`Product Created - ${this.payload.reference}`)
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
                    r_createProduct(this.payload,this.onProductCreated)
                }
            }
        },  
        mounted(){
            
        }
    }
</script>