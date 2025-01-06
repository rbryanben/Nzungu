<template>
    <div class="wrapper">
        <div class="input-wrapper">
            <img src="/svg/search.svg" alt="">
            <input required :class="{'error' : inputError }" :placeholder="hint" v-model="value" @input="onTextChanged" :type="type">
        </div>
    </div>
</template>

<style lang="css" scoped>

    .wrapper {
        position: relative;
    }

    input {
        border: none;
        min-height: 35px;
        min-width: 600px;
        outline: solid 1.8px rgba(128, 128, 128, 0.181);
        background-color: rgba(163, 163, 163, 0.084);
        border-radius: 10px;
        padding-left: 30px;
        font-size: 0.9rem;
        transition: all 0.1s ease-in;
        color: rgb(32, 32, 32);
    }

    input:focus {
        outline: solid 1.8px rgba(243, 138, 27, 0.86);
        background-color: white;
        min-width: 600px;
    }

    input:focus~img {
        opacity: 0.2;
    }

    input:valid {
        background-color: white;
        min-width: 600px;
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
        object-fit: contain;
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