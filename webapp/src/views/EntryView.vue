<template>
    <div class="entry-view-wrapper">
        <img src="/img/icons/android-chrome-512x512.png">
    </div>
</template>

<style scoped>
    .entry-view-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100vw;
        overflow-x: hidden;
    }

    img {
        transform: translateY(-10%);
        height: 80px;
        animation:  zoom_in ease-in 0.4s;
    }

    @keyframes zoom_in {
        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }
</style>

<script>
    import { ENDPOINTS } from '@/main';
import { getEmployeeDetails } from '@/repo/SaleRepo';
import { notify_failed, notify_success } from '@/utils/notifications';

    export default {
        name : 'EntryView',
        methods: {
            // On employee result 
            onGetEmployeeResult(success,payload){
                if (success){
                    this.$router.replace({name: "sales"})
                }
            },
            // initialization method 
            init(){
                // Check for authentication 
                getEmployeeDetails(this.onGetEmployeeResult)
            }
        },
        mounted(){
            // Initialize
            this.init()
        }
    }
</script>