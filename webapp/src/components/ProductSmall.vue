<template>
    <div class="product-small-wrapper">
        <div class="left">
            <img class="product-image" :src="image_url" />
        </div>
        <div class="right">
            <div class="title">
                {{ product_name }}
            </div>
            <div class="count">
                x{{ cart_count }}
            </div>
            <div class="category">
                {{ product_description }}
            </div>
            <div class="total-price">
                $<b>{{ display_price.toFixed(2) }}</b>
            </div>
        </div>
    </div>
</template>

<style lang="css" scoped>
    .product-small-wrapper {
        display: grid;
        grid-template-columns: 60px auto;
        height: fit-content;
        position: relative;
    }

    .product-image {
        height: 50px;
        width: 50px;
        object-fit: contain;
    }

    .title {
        font-size: 1rem;
        font-weight: bold;
        width: 80%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .count {
        font-size: 0.7rem;
        margin-top: -2px;
    }

    .category {
        margin-top: 7px;
        font-size: 0.9rem;
        width: 60%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .total-price {
        position: absolute;
        right: 25px;
        bottom: 0px;
        font-size: 0.9rem;
    }

    @media only screen and (max-width: 1200px) {
        .product-small-wrapper {
            grid-template-columns: 40px auto;
        }

        .product-image {
            height: 35px;
            width: 35px;
        }

        .title {
            font-size: 0.8rem;
            width: 70%;
        }

        .count {
            font-size: 0.6rem;
            margin-top: -2px;
        }

        .category {
            margin-top: 2px;
            font-size: 0.6rem;
            width: 55%;
        }

        .total-price {
            position: absolute;
            right: 10px;
            font-size: 0.7rem;
        }
    }

    @media only screen and (max-width: 750px) {

    }
</style>

<script>
    export default {
        name : "ProductSmall",
        data(){
            return {
                name : "Product Small"
            }
        },
        props: {
            product_name : {
                type: String,
                default: "product-name"
            },
            cart_count : {
                type: Number,
                default: 1
            },
            product_description : {
                type: String,
                default: "product-description"
            },
            display_price : {
                type: Number,
                default: 0
            },
            image_url : {
                type: String,
                default: "product-name"
            }
        }
    }
</script>