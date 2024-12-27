<template>
    <div class="wrapper">
        <div class="input-title">
            {{title}}
        </div>
        <div class="input-wrapper">
            <input :class="{'error' : inputError }" :placeholder="placeholder" v-model="value" @input="onTextChanged" :type="type">
        </div>
    </div>
</template>

<style lang="css" scoped>

    .input-title {
        font-size: 0.9rem;
        color: rgb(46, 46, 46);
    }

    .input-wrapper {
        margin-top: 5px;
    }

    input {
        border: none;
        min-height: 30px;
        min-width: 300px;
        outline: solid 1.2px grey;
        border-radius: 5px;
        padding-left: 8px;
        transition: all 0.1s ease-in;
    }

    input:focus {
        outline: solid 1.3px rgb(62, 62, 62);
    }

    input.error {
        outline: solid 1.3px rgb(193, 0, 0);
    }
</style>

<script>
    import validators from "../shared/validators"

    export default {
        name: "TitledInput",
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
            placeholder : {
                type: String,
                default: ""
            },
            validator : {
                type: String,
                default: 'username'
            }
        }
    }
</script>