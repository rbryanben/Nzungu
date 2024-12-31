<template>
    <div class="selector-wrapper">
        <div class="selector" :class="{'two' : selected == 1}">
        </div>
        <div class="item" :class="{'selected' : selected == 0}" @click=" onSelect(0)">
            <img src="/svg/us.svg" />
        </div>
        <div class="item" :class="{'selected' : selected == 1}" @click=" onSelect(1)">
            <img src="/svg/zw.svg" />
        </div>
    </div>
</template>

<style lang="css" scoped>
    .selector-wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-column-gap: 2px;
        padding: 7px 8px;
        width: fit-content;
        background-color: #f2f1f2;;
        font-size: x-small;
        border-radius: 17px;
        border: solid 1.2px rgba(128, 128, 128, 0.301);
        position: relative;
        cursor: pointer;
    }

    .selector-wrapper .item {
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 2;
    }

    .selector-wrapper .item.selected {
        font-weight: bold;
    }

    .selector {
        background-color: rgba(243, 139, 27, 0.308);
        width: calc(50% + 2px);
        height: 100%;
        display: flex;
        position: absolute;
        border-radius: inherit;
        z-index: 1;
        margin: 0.2px;
        transition: all 0.1s ease-in;
    }

    .selector.two {
        left: calc(50% - 2px);
        transition: all 0.1s ease-in;
    }

    img {
        height: 15px;
        width: 15px;
        margin: 0 5px;
    }


</style>
<script>
    export default {
        name : "TwinSelector",
        data(){
            return {
                selected: 0
            }
        },
        methods: {
            onSelect(index){
                this.$emit('on-select-changed',index)
                this.selected = index
            }
        }
    }
</script>