<template>
    <div class="wrapper">
        <div class="top">
            <img src="/svg/money-bill-transfer.svg" alt="" class="icon"> <span>{{title}}</span> 
        </div>
        <div class="middle">
            {{currency}} ${{formatTwoDecimals(amount)}}
        </div>
        <div class="bottom">
            <div class="left" :class="{'perfomance-decrease' : performance < 0}">
                <img v-if="performance >= 0" src="/svg/chart-line-up.svg" alt=""> 
                <img v-else src="/svg/chart-line-down.svg" alt=""> 
                {{performance}}%
            </div>
            <div class="right">
                {{periodText}}
            </div>
        </div>
    </div>
</template>

<style scoped>
    .wrapper {
        background-color: white;
        width: fit-content;
        font-size: 0.9rem;
        border-radius: 8px;
        padding: 10px;
        cursor: pointer;
        width: 190px;
    }

    .wrapper .top {
        display: flex;
        font-size: 1rem;
        font-weight: bold;
    }

    .wrapper .top span {
        margin-top: 1px;
    }

    .wrapper .top img {
        height: 20px;
        width: 20px;
        opacity: 0.4;
        margin-right: 10px
    }

    .wrapper .middle {
        margin-top: 30px;
        font-size: 1.45rem;
    }

    .wrapper .bottom {
        margin-top: 10px;
        display: flex;
        font-size: 0.7rem;
    }

    .wrapper .bottom .left {
        background-color: rgba(178, 237, 178, 0.296);
        font-weight: bold;
        padding: 5px;
        border-radius: 5px;
        display: flex;
    }

    .wrapper .bottom .left.perfomance-decrease {
        background-color: rgba(237, 182, 178, 0.296);
    }

    .wrapper .bottom .left img {
        height: 12px;
        margin-right: 5px;
    }
    .wrapper .bottom .right {
        margin-top: 5px;
        margin-left: 5px;
    }

    @media only screen and (max-width: 1200px) {
        .wrapper {
            font-size: 0.8rem;
            width: 160px;
        }

        .wrapper .middle {
            margin-top: 15px;
            font-size: 1.1rem;
        }

        .wrapper .bottom {
            margin-top: 10px;
            display: flex;
            font-size: 0.6rem;
        }

    }

</style>

<script>
    import { formatTwoDecimals } from '@/utils/common';

    export default {
        name : "CurrencyValueTile",
        methods: {
            formatTwoDecimals: formatTwoDecimals
        },
        props: {
            currency: {
                type: String,
                default: "USD"
            },
            amount: {
                type: Number,
                default: 0
            },
            periodText: {
                type: String,
                default: "From yesterday"
            },
            performance : {
                type: Number,
                default: 0
            },
            title: {
                type: String,
                default: "Total Cash"
            }
        }
    }
</script>
