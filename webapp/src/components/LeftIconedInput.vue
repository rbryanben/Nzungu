<template>
    <div class="wrapper">
        <img src="/svg/search.svg" alt="">
        <div class="input-wrapper">
            <input :class="{'error' : inputError }" :placeholder="hint" v-model="value" @input="onTextChanged" :type="type">
        </div>
    </div>
</template>

<style lang="css" scoped>

    .wrapper {
        position: relative;
    }

    input {
        border: none;
        min-height: 28px;
        min-width: 400px;
        outline: solid 1.2px rgba(128, 128, 128, 0.301);
        border-radius: 10px;
        padding-left: 30px;
        font-size: 0.8rem;
        transition: all 0.1s ease-in;
        color: rgb(32, 32, 32);
    }

    input:focus {
        outline: solid 1.8px rgba(243, 138, 27, 0.86);
    }

    input.error {
        outline: solid 1.5px rgb(193, 0, 0);
    }

    img {
        height: 15px;
        width: 15px;
        opacity: 0.7;
        position: absolute;
        left: 8px;
        top: 50%;
        transform: translateY(-50%);
    }
</style>

<script>
    import validators from "../shared/validators"

    export default {
        name: "LeftIconedInput",
        data(){
            return {
                value: ""
            }
        },
        methods: {
            onTextChanged(){
                this.$emit("on-text-changed",this.value)
            }  
        },
        mounted(){
            console.log(validators)
        },
        computed: {
            inputError(){
                if (this.value == "") return false
                return !validators[this.validator](this.value)
            }
        },
        props: {
            title : {
                type: String,
                default: "TitledInput"
            },
            hint : {
                type: String,
                default: ""
            },
            type : {
                type: String,
                default: "text"
            },
            validator : {
                type: String,
                default: 'username'
            }
        }
    }
</script>