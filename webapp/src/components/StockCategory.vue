<template>
    <div class="wrapper button-effect">
        <div class="left">
            <img :src="valid_icon" />
        </div>
        <div class="right">
            <div class="top">
                {{name}}
            </div>
            <div class="bottom">
                {{ stock_count }} Items In Stock
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
        padding: 20px;
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

    @media only screen and (max-width: 1200px) {
        .wrapper {
            grid-template-columns: 15px 80px;
            padding: 8px;
        }

        .wrapper .left img {
            height: 17px;
            width: 17px;
            opacity: 0.6;
        }

        .wrapper .right .top {
            font-size: 0.7rem;
            margin-bottom: 2px;
        }

        .wrapper .right .bottom {
            font-size: 0.6rem;
            color: rgba(75, 75, 75, 0.868);
            margin-top: 2px;
        }
    }

    @media only screen and (max-width: 700px) {
        .wrapper {
            grid-template-columns: 10px 70px;
            padding: 8px;
        }

        .wrapper .left img {
            height: 14px;
            width: 14px;
            opacity: 0.6;
        }

        .wrapper .right .top {
            font-size: 0.6rem;
            margin-bottom: 2px;
        }

        .wrapper .right .bottom {
            font-size: 0.5rem;
            color: rgba(75, 75, 75, 0.868);
            margin-top: 2px;
        }
    }

</style>

<script>
    export default {
        name : "StockCategory",
        computed: {
            valid_icon(){
                
                const iconSet = new Set([
                    "cheese-swiss.svg",
                    "bread-loaf.svg",
                    "can-food.svg",
                    "bottle-water.svg",
                    "cookie.svg",
                    "soap.svg",
                    "baby.svg"
                ]);


                if (iconSet.has(this.icon)){
                    return '/svg/' + this.icon
                }
                
                return '/svg/burger-soda.svg'
            }
        },
        props: {
            name: {
                type: String,
                default: "category-name"
            },
            stock_count: {
                type: Number,
                default: 0
            },
            ref : {
                type: String,
                default: "category-ref"
            },
            icon : {
                type: String,
                default: "/svg/burger-soda.svg"
            }
        }
    }
</script>