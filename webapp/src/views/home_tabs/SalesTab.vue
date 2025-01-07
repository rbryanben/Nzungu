<template>
    <div class="sales-wrapper">
        <!-- Tool Bar  -->
        <div class="tool-bar">
            <div class="search-box-wrapper">
                <LeftIconedInput validator="none" hint="Search your products here"/>
            </div>
            <div class="currency-icon-wrapper">
                <TwinSelector />
            </div>
            <div class="notification-icon-wrapper">
                <img src="/svg/bell.svg" alt="" class="bell">
            </div>
            <div class="profile-wrapper">
                <div class="dp align-center">
                    <img src="\samples\dp.jpg" />
                </div>
                <div class="content">
                    <div style="height: fit-content;" class="align-center">
                        <div class="fullname">Samson Nyalugwe</div>
                        <div class="title">Shop Manager</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- bottom  -->
        <div class="bottom">
            <!-- left -->
            <div class="left">
                <div class="categories">
                    <div class="category-wrapper">
                        <StockCategory />
                    </div>
                </div>
                <div class="products">
                    <div class="product-wrapper">
                        <Product />
                    </div>
                </div>                                                                  
            </div>
            <!-- Right -->
            <div class="right">
                R
            </div>
        </div>

    </div>
</template>

<style lang="css" scoped>
    .sales-wrapper {
        width: 100%;
        height: 100%;
    }

    .tool-bar {
        background-color: white;
        height: 45px;
        max-height: 45px;
        padding-left: 20px;
        padding-top: 10px;
        padding-bottom: 10px;
        border-bottom: solid 1.8px rgba(128, 128, 128, 0.116);
        display: grid;
        grid-template-columns: 0.78fr 0.03fr 0.05fr 0.1fr;
    }

    .search-box-wrapper{
        display: flex;
        align-items: center;
        margin-left: 20%;
    }
    .notification-icon-wrapper, .currency-icon-wrapper {
       display: flex;
       justify-content: center;
       align-items: center;
    }

    img.bell {
        height: 15px;
        width: 15px;
    }

    .profile-wrapper {
        display: grid;
        grid-template-columns: 35px auto;
        grid-column-gap: 5px;
    }

    .profile-wrapper .dp img {
        border-radius: 50%;
        height: 35px;
        width: 35px;
    }

    .profile-wrapper .content {
        display: flex;
        justify-content: center;
        transform: translateY(-1px);
    }
    .profile-wrapper .content .fullname {
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 1px;
        margin-top: auto;
    }

    .profile-wrapper .content .title{
        font-size: 0.7rem;
    }

    .align-center {
        margin-top: auto;
        margin-bottom: auto;
    }

    .bottom {
        display: grid;
        padding: 20px;
        padding-top: 10px;
        grid-template-columns: calc(100% - 350px) 350px;
        min-height: calc(100% - 96.78px);
        max-height: calc(100% - 96.78px);
    }

    .categories {
        display: flex;
        flex-wrap: wrap;
        gap: 5px 10px;
        width: 100%;
    }

    .products {
        padding-top: 20px;
    }
</style>

<script>
    import LeftIconedInput from "../../components/LeftIconedInput"
    import TwinSelector from "@/components/TwinSelector.vue";
    import StockCategory from "@/components/StockCategory.vue";
    import Product from "@/components/Product.vue";
   
    export default {
        name: "SalesTab",
        components: {
            LeftIconedInput,
            TwinSelector,
            StockCategory,
            Product
        },
        data(){
            return {
                name: "Sales Tab Benso"
            }
        }
    }
</script>