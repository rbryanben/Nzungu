<template>
    <!-- Tool Bar  -->
    <div class="tool-bar">
        <div class="search-box-wrapper">
            <LeftIconedInput validator="none" v-on:on-text-changed="onSearchTextChanged" hint="Search your products here"/>
        </div>
        <div class="currency-icon-wrapper">
            <TwinSelector @on-select-changed="onCurrencyChange" />
        </div>
        <div class="notification-icon-wrapper">
            <img src="/svg/rotate-reverse.svg" alt="" title="Refresh Page" @click="refreshPage" class="bell">
        </div>
        <div class="profile-wrapper">
            <div class="dp align-center">
                <img src="\samples\dp.jpg" />
            </div>
            <div class="content">
                <div style="height: fit-content;" class="align-center">
                    <div class="fullname">{{$store.state.sales.employee.name}}</div>
                    <div class="title">{{$store.state.sales.employee.role}}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .tool-bar {
        background-color: white;
        height: 45px;
        max-height: 45px;
        padding-left: 20px;
        padding-top: 10px;
        padding-bottom: 10px;
        border-bottom: solid 1.8px rgba(128, 128, 128, 0.116);
        display: grid;
        grid-template-columns: 0.78fr 0.03fr 0.05fr 0.1fr;
    }

    .search-box-wrapper{
        display: flex;
        align-items: center;
        margin-left: 20%;
    }
    .notification-icon-wrapper, .currency-icon-wrapper {
       display: flex;
       justify-content: center;
       align-items: center;
    }

    img.bell {
        height: 25px;
        width: 25px;
        opacity: 0.8;
        cursor: pointer;
    }

    .profile-wrapper {
        display: grid;
        grid-template-columns: 35px auto;
        grid-column-gap: 5px;
    }

    .profile-wrapper .dp img {
        border-radius: 50%;
        height: 35px;
        width: 35px;
    }

    .profile-wrapper .content {
        display: flex;
        justify-content: center;
        transform: translateY(-1px);
    }
    .profile-wrapper .content .fullname {
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 1px;
        margin-top: auto;
    }

    .profile-wrapper .content .title{
        font-size: 0.7rem;
    }

    .align-center {
        margin-top: auto;
        margin-bottom: auto;
    }

    @media only screen and (max-width: 1200px) {
        .bottom {
            grid-template-columns: auto 240px;
        }
        
        .tool-bar {
            background-color: white;
            height: 45px;
            max-height: 45px;
            padding-left: 20px;
            padding-top: 10px;
            padding-right: 10px;
            padding-bottom: 10px;
            border-bottom: solid 1.8px rgba(128, 128, 128, 0.116);
            display: grid;
            grid-template-columns: auto 80px 70px 100px;
        }

        .search-box-wrapper{
            width: 100%;
            margin-left: 0%;
        }
    }

</style>

<script>
    import LeftIconedInput from './LeftIconedInput.vue';
    import TwinSelector from './TwinSelector.vue';

    export default {
        name : "ToolBar",
        components: {
            LeftIconedInput,
            TwinSelector
        },
        methods: {
            onSearchTextChanged(payload){
                this.$emit("on_search_text_changed",payload)
            },
            onCurrencyChange(){

            },
            refreshPage(){
                this.$emit('refresh-page')
            }
        }

    }
</script>