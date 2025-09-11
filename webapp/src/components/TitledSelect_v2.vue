<template>
    <div class="wrapper">
        <div class="select-title">
            {{title}}
        </div>
        <div class="select-wrapper">
            <select 
                required 
                :class="{'fill' : fill}" 
                :disabled="!editable" 
                :placeholder="placeholder" 
                :value="modelValue"
                @change="$emit('update:modelValue', $event.target.value);">
                <option 
                    v-for="option in options" 
                    :key="option.ref" 
                    :value="option.ref">{{option.name}}</option>
            </select>
        </div>
    </div>
</template>

<style lang="css" scoped>

    .select-title {
        font-size: 0.9rem;
        color: rgb(46, 46, 46);
    }

    .select-wrapper {
        margin-top: 5px;
    }

    select {
        border: none;
        min-height: 30px;
        min-width: 300px;
        outline: solid 1.8px rgba(128, 128, 128, 0.181);
        background-color: rgba(163, 163, 163, 0.084);
        border-radius: 5px;
        padding-left: 8px;
        transition: all 0.1s ease-in;
    }

    select.fill {
        width: calc(100% - 2px);
    }

    select:focus {
        outline: solid 1.8px rgba(243, 138, 27, 0.86);
        background-color: white;
    }

    select:valid {
        background-color: white;
    }

    select.error {
        outline: solid 1.8px rgb(193, 0, 0);
    }
</style>

<script>
    export default {
        name: "TitledSelect_v2",
        props: {
            title : {
                type: String,
                default: "TitledSelect"
            },
            hint : {
                type: String,
                default: ""
            },
            placeholder : {
                type: String,
                default: ""
            },
            fill: {
                type: Boolean,
                default: false
            },
            editable: {
                type: Boolean,
                default: true
            },
            options: {
                type: Array,
                default: []
            },
            modelValue: {
                type: String,
                default: ""
            }
        }
    }
</script>