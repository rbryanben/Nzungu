<template>
    <div class="wrapper">
        <div class="top">
            <div class="left">
                <img :src="image" alt="">
            </div>
            <div class="right">
                <div class="name">{{name}}</div>
                <div class="description">
                    {{ description}}
                </div>
                <div class="stock-count">
                    {{ stock }} Items in stock
                </div>
            </div>
        </div>
        <div class="bottom">
            <div class="left">
                $<span style="font-weight: bold;color: #404143;">{{ price }}</span>  
            </div>
            <div class="right-buttons">
                <div class="sub circle-button" @mousedown="increment(-1)">
                    -
                </div>
                <div class="quantity">
                    {{ count }}
                </div>
                <div class="add circle-button" :class="{'in-cart':count > 0}"  @click="increment()">
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
        width: 305px;
        max-width: 305px;
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
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 195px;
    }

    .wrapper .top .right .description {
        font-size: 0.9rem;
        color: rgb(90, 89, 89);
        margin-top: 8px;
        min-width: 180px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 195px;
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
        pointer-events: none;
    }

    .wrapper .bottom .right-buttons .quantity {
        margin-left: 9px;
        margin-right: 9px;
        margin-top: auto;
        margin-bottom: auto;
        
    }

    .circle-button {
        display: flex;
        pointer-events: all;
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

    .add {
        color: rgb(40, 119, 165);
    }

    .in-cart {
        background-color: rgb(40, 130, 165);
        color: white;
    }

    
    @media only screen and (max-width: 1200px) {
        .wrapper {
            width: 200px;
            max-width: 200px;
            padding: 6px;
        }

        .wrapper .top {
            display: grid;
            grid-column-gap: 8px;
            grid-template-columns: 1.5fr auto;
        }
        
        .wrapper img {
            height: 40px;
            width: 40px;
        }

         .wrapper .top .right .name {
            font-size: 0.8rem;
            width: 140px;
        }

        .wrapper .top .right .description {
            font-size: 0.7rem;
            width: 140px;
        }

        
        .wrapper .bottom .right-buttons {
            display: flex;
            margin-left: auto;
            margin-right: 0px;
            cursor: pointer;
        }

    }

    @media only screen and (max-width: 750px) {
        .wrapper {
            width: 150px;
            max-width: 150px;
            padding: 6px;
        }

        .wrapper .top {
            display: grid;
            grid-column-gap: 8px;
            grid-template-columns: 38px auto;
        }
        
        .wrapper img {
            height: 30px;
            width: 30px;
        }

         .wrapper .top .right .name {
            font-size: 0.7rem;
            width: 140px;
        }

        .wrapper .top .right .description {
            font-size: 0.6rem;
            width: 140px;
        }

        .wrapper .top .right .stock-count {
            font-size: 0.5rem;
        }

        .wrapper .bottom .left {
            font-size: 1.1rem;
        }

        .wrapper .bottom .right-buttons {
            transform: scale(0.8);
        }

    }

</style>

<script>
    export default {
        name : "Product",
        data(){
            return {
                count : 0
            }
        },
        methods: {
            increment(count=1){
                this.count = Math.max(0,this.count + count)
                // Emit
                this.$emit('on_update_product',count)
            }
        },
        props: {
            ref : {
                type: String,
                default: "product-ref"
            },
            name : {
                type: String,
                default: "product-name"
            },
            description : {
                type: String,
                default: "product-description"
            },
            stock : {
                type: Number,
                default: 0
            },
            image: {
                type: String,
                default: "/samples/king-curls.jpg"
            },
            price : {
                type: Number,
                default: 0
            },
            
        }
    }
</script>