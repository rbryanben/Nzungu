<template>
    <div class="wrapper" :class="[{ 'disabled' : disabled},theme,size]" @click="onClick">
        <div v-if="!loading">{{ text }}</div>
        <div v-if="loading" class="loader-wrapper">
            <div class="lds-roller"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
        </div>
    </div>
</template>

<style lang="css" scoped>

   .wrapper {
        position: relative;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 0.9rem;
        cursor: pointer;
        background-color: rgb(63, 63, 63);
        overflow: hidden;
        min-height: 20px;
        transition: all 0.2s ease-in;
    }


    .wrapper.orange {
        background-color: rgba(243, 138, 27, 0.86);
    }

    .wrapper.disabled {
        pointer-events: none;
        opacity: 0.5;
    }
    .loader-wrapper {
        height: 10px;
        position: absolute;
        top: 25%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.3);
    }

    .lds-roller {
    /* change color here */
    color: #ffffff
    }
    .lds-roller,
    .lds-roller div,
    .lds-roller div:after {
    box-sizing: border-box;
    }
    .lds-roller {
    display: inline-block;
    position: relative;
    width: 40px;
    height: 40px;
    }
    .lds-roller div {
    animation: lds-roller 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    transform-origin: 40px 40px;
    }
    .lds-roller div:after {
    content: " ";
    display: block;
    position: absolute;
    width: 7.2px;
    height: 7.2px;
    border-radius: 50%;
    background: currentColor;
    margin: -3.6px 0 0 -3.6px;
    }
    .lds-roller div:nth-child(1) {
    animation-delay: -0.036s;
    }
    .lds-roller div:nth-child(1):after {
    top: 62.62742px;
    left: 62.62742px;
    }
    .lds-roller div:nth-child(2) {
    animation-delay: -0.072s;
    }
    .lds-roller div:nth-child(2):after {
    top: 67.71281px;
    left: 56px;
    }
    .lds-roller div:nth-child(3) {
    animation-delay: -0.108s;
    }
    .lds-roller div:nth-child(3):after {
    top: 70.90963px;
    left: 48.28221px;
    }
    .lds-roller div:nth-child(4) {
    animation-delay: -0.144s;
    }
    .lds-roller div:nth-child(4):after {
    top: 72px;
    left: 40px;
    }
    .lds-roller div:nth-child(5) {
    animation-delay: -0.18s;
    }
    .lds-roller div:nth-child(5):after {
    top: 70.90963px;
    left: 31.71779px;
    }
    .lds-roller div:nth-child(6) {
    animation-delay: -0.216s;
    }
    .lds-roller div:nth-child(6):after {
    top: 67.71281px;
    left: 24px;
    }
    .lds-roller div:nth-child(7) {
    animation-delay: -0.252s;
    }
    .lds-roller div:nth-child(7):after {
    top: 62.62742px;
    left: 17.37258px;
    }
    .lds-roller div:nth-child(8) {
    animation-delay: -0.288s;
    }
    .lds-roller div:nth-child(8):after {
    top: 56px;
    left: 12.28719px;
    }
    @keyframes lds-roller {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
    }

 

    .wrapper::before {
        content: '';
        display: flex;
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0px;
        height: 200px;
        background-color: rgba(191, 191, 191, 0.096);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: all 0.2s ease-in;
    }

    .wrapper:hover::before {
        width: 100%;
    }
    
    @media only screen and (max-width: 1200px) {
        .wrapper {
            padding: 5px 3px;
            font-size: 0.7rem;
        }
    }

</style>

<script>
    export default {
        name: "PlainButton",
        props: {
            text: {
                type: String,
                default: "PlainButton"
            },
            loading: {
                type: Boolean,
                default: false
            },
            disabled: {
                type: Boolean,
                default: false
            },
            theme: {
                type: String,
                default: "dark"
            },
            size : {
                type: String,
                default: 'normal'
            }
        },
        methods: {
            onClick(){
                this.$emit('on-click',this.loading)
            }
        }
    }
</script>
