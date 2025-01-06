<template>
    <div class="wrapper">
        <div class="top">
            <div class="left">
                <img src="/samples/king-curls.jpg" alt="">
            </div>
            <div class="right">
                <div class="name">King Kurls</div>
                <div class="description">
                    Curly snack 100g packs.
                </div>
                <div class="stock-count">
                    22 Items in stock
                </div>
            </div>
        </div>
        <div class="bottom">
            <div class="left">
                $<span style="font-weight: bold;color: #404143;">0.50</span>  
            </div>
            <div class="right-buttons">
                <div class="sub circle-button">
                    -
                </div>
                <div class="quantity">
                    2
                </div>
                <div class="add circle-button">
                    +
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .wrapper {
        padding: 10px;
        border-radius: 10px;
        background-color: white;
        width: fit-content;
    }

    .button-effect::after {
        content: "";
        display: flex;
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        height: 100%;
        background-color: rgba(212, 212, 212, 0.179);
        width: 0px;
        transition: all 0.3s ease-in;
        border-radius: inherit;
        transform-origin: center;
        z-index:1;
        
    }

    .button-effect:hover:after{
        width: 240%;
    }
    .wrapper .top {
        display: grid;
        grid-column-gap: 15px;
        grid-template-columns: 0.2fr 0.8fr;
    }

    .wrapper .top .right .name {
        font-weight: bold;
        font-size: 1rem;
    }

    .wrapper .top .right .description {
        font-size: 0.9rem;
        color: rgb(90, 89, 89);
        margin-top: 8px;
        min-width: 180px;
    }

    .wrapper .top .right .stock-count {
        font-size: 0.7rem;
        font-weight: bold;
        margin-top: 4px;
        color: rgb(44, 81, 45);
    }

    .wrapper img {
        height: 80px;
        width: 80px;
        border-radius: 5px;
        object-fit: cover;
    }

    .wrapper .bottom {
        display: grid;
        margin-top: 5px;
        grid-template-columns: 1fr 1fr;
    }

    .wrapper .bottom .left {
        font-size: 1.2rem;
        color: gray;
        margin-top: auto;
        margin-bottom: auto;
        margin-left: 10px;
    }

    .wrapper .bottom .right-buttons {
        display: flex;
        background-color: #f2f1f2;
        border-radius: 15px;
        padding: 1px 2px;
        width: fit-content;
        margin-left: auto;
        cursor: pointer;
    }

    .wrapper .bottom .right-buttons .quantity {
        margin-left: 9px;
        margin-right: 9px;
        margin-top: auto;
        margin-bottom: auto;
        
    }

    .circle-button {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px;
        height: 10px;
        width: 10px;
        border-radius: 50%;
        font-size: 1.2rem;
        background-color: white;
        border: solid 1.8px rgba(128, 128, 128, 0.181);
        transition: all 0.2s ease-in;
    }

    .circle-button:hover{
        background-color: rgb(243, 243, 243);
    }

    .add {
        color: rgb(40, 119, 165);
    }
</style>

<script>
    export default {
        name : "Product"
    }
</script>