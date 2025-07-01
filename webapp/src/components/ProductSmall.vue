<template>
    <div class="product-small-wrapper">
        <div class="left">
            <img class="product-image" src="/samples/king-curls.jpg" />
        </div>
        <div class="right">
            <div class="title">
                Pasta Bolognese
            </div>
            <div class="count">
                x2
            </div>
            <div class="category">
                Fruits and Vegetables
            </div>
            <div class="total-price">
                $<b>50.5</b>
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
        object-fit: cover;
    }

    .title {
        font-size: 1rem;
        font-weight: bold;
    }

    .count {
        font-size: 0.7rem;
        margin-top: -2px;
    }

    .category {
        margin-top: 7px;
        font-size: 0.9rem;
    }

    .total-price {
        position: absolute;
        right: 25px;
        bottom: 0px;
        font-size: 0.9rem;
    }
</style>

<script>
    export default {
        name : "ProductSmall",
        data(){
            return {
                name : "Product Small"
            }
        }
    }
</script>