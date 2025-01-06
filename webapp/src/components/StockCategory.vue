<template>
    <div class="wrapper button-effect">
        <div class="left">
            <img src="/svg/burger-soda.svg" />
        </div>
        <div class="right">
            <div class="top">
                Breakfast
            </div>
            <div class="bottom">
                24 Items In Stock
            </div>
        </div>
    </div>
</template>

<style scoped>
    .wrapper {
        display: grid; 
        grid-template-columns: 40px 150px;
        background-color: white;
        cursor: pointer;
        padding: 15px;
        width: fit-content;
        border-radius: 8px;
        grid-column-gap: 8px;
        border: solid 1.8px rgba(128, 128, 128, 0.116);        
    }

    .button-effect {
        position: relative;
        overflow: hidden;
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

    .wrapper .left {
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2;
    }

    .wrapper .left img {
        height: 30px;
        width: 30px;
        opacity: 0.6;
    }

    .wrapper .right {
        z-index: 2;
    }

    .wrapper .right .top {
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 5px;
        color: rgba(46, 46, 46, 0.773);
    }


    .wrapper .right .bottom {
        font-size: 0.8rem;
        color: rgba(75, 75, 75, 0.868);
        margin-top: 5px;
    }


</style>

<script>
    export default {
        name : "StockCategory"
    }
</script>