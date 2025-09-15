<template>
    <div class="wrapper">
        <div class="input-title">
            {{title}}
        </div>
        <div class="input-wrapper">
            <input 
                required 
                :class="{'error' : inputError, 'fill' : fill}" 
                :disabled="!editable" 
                :placeholder="placeholder" 
                :value="modelValue" 
                :type="type"
                @input="$emit('update:modelValue', $event.target.value)">
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
        outline: solid 1.8px rgba(128, 128, 128, 0.181);
        background-color: rgba(163, 163, 163, 0.084);
        border-radius: 5px;
        padding-left: 8px;
        transition: all 0.1s ease-in;
    }

    input.fill {
        width: calc(100% - 9px);
    }

    input:focus {
        outline: solid 1.8px rgba(243, 138, 27, 0.86);
        background-color: white;
    }

    input:valid {
        background-color: white;
    }

    input.error {
        outline: solid 1.8px rgb(193, 0, 0);
    }
</style>

<script>
    import validators from "../shared/validators"

    export default {
        name: "TitledInput_v2",
        computed: {
            inputError(){
                if (this.modelValue === "" || this.modelValue == 0 || isNaN(this.modelValue) || this.modelValue == null){
                    return false
                }

                return !validators[this.validator](this.modelValue)
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
            },
            fill: {
                type: Boolean,
                default: false
            },
            editable: {
                type: Boolean,
                default: true
            },
            modelValue: {
                type: String,
                default: ""
            }
        }
    }
</script>