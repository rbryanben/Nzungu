<template>
    <div class="wrapper" :class="{'selected' : selected}">
        <div class="top">
            <div class="left">
                <div class="shadow" :style="{backgroundColor: theme}">
                    <img :src="valid_icon">
                </div>
            </div>
            <div class="right">
                {{caption}}
            </div>
        </div>
        <div class="middle">
            {{ subtext }}
        </div>
        <div class="bottom">
            <b>{{count}}</b>
        </div>
    </div>
</template>

<style scoped>
    .wrapper {
        background-color: white;
        width: fit-content;
        font-size: 0.7rem;
        border-radius: 8px;
        padding: 10px;
    }

    .wrapper.selected{
        background-color: rgb(251, 249, 245);
        outline: solid 1.2px rgba(255, 207, 117, 0.348);
    }

    .top {
        display: grid;
        grid-template-columns: 30px 100px;
        grid-column-gap: 10px;
    }

    .top .left .shadow {
        background-color: rgba(185, 185, 185, 0.207);
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
    }

    .top .right {
        margin-top: 8px;
        font-weight: bold;
    }

    .top img {
        height: 12px;
        widows: 12px;
        opacity: 0.6;
    }

    .middle {
        margin-top: 8px;
        font-size: 0.6rem;
    }

    .bottom {
        margin-top: 5px;
    }
</style>

<script>
    export default {
        name : "SummaryTile",
        computed: {
            valid_icon(){
                return `/svg/${this.icon}.svg`
            }       
        },
        props : {
            icon: {
                type : String,
                default: "box-archive"
            },
            caption : {
                type: String,
                default: "caption-here"
            },
            theme: {
                type: String,
                default: "background-color: rgba(185, 185, 185, 0.207)"
            },
            subtext : {
                type: String,
                default: "subtext-here"
            },
            count: {
                type: Number,
                default: 0
            },
            selected : {
                type: Boolean,
                default: false
            }
        }

    }
</script>
