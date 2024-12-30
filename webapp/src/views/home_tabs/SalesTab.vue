<template>
    <div class="sales-wrapper">
        <div class="tool-bar">
            <div class="search-box-wrapper">
                <LeftIconedInput validator="none" hint="Search your products here"/>
            </div>
            <div class="currency-icon-wrapper">
                <TwinSelector />
            </div>
            <div class="notification-icon-wrapper">
                i
            </div>
            <div class="profile-wrapper">
                P
            </div>
        </div>
    </div>
</template>

<style lang="css" scoped>
    .sales-wrapper {
        width: 100%;
        height: 100%;
    }

    .tool-bar {
        background-color: white;
        height: 45px;
        max-height: 45px;
        padding-left: 20px;
        padding-top: 10px;
        border-bottom: solid 1.5px rgba(128, 128, 128, 0.301);
        display: grid;
        grid-template-columns: 0.8fr 0.05fr 0.05fr 0.1fr;
    }

</style>

<script>
    import LeftIconedInput from "../../components/LeftIconedInput"
    import TwinSelector from "@/components/TwinSelector.vue";
    
    export default {
        name: "SalesTab",
        components: {
            LeftIconedInput,
            TwinSelector
        },
        data(){
            return {
                name: "Sales Tab Benso"
            }
        }
    }
</script>