<template>
    <div class="login-wrapper">
        <div class="card align-fixed-center">
            <!-- Username -->
            <div class="title" style="text-align: center;">Welcome back</div>
            <!-- Greeting -->
            <div style="margin-top: 10px; text-align: center;" class="subtitle">
                Glad to see you again 👋<br>Login to your account below
            </div>
            <!-- Username -->
            <div style="margin-top: 40px;" class="input-wrapper">
                <TitledInput title="Username" validator="username" :fill="true"  v-on:on-text-changed="(e)=>{formChange('username',e)}" placeholder="Type your username"/>
            </div>
            <!-- Password -->
            <div class="input-wrapper">
                <TitledInput  title="Password" validator="password" :fill="true" v-on:on-text-changed="(e)=>{formChange('password',e)}" type="password" placeholder="Type your password"/>
            </div>
            <!-- Login -->
            <div class="button-wrapper">
                <PlainButton text="Login" v-on:on-click="onLoginClicked" :loading="submitting" :disabled="disableSubmit"/>
            </div>
            <!-- Legend -->
            <div class="legend">
                About the project <a href="https://github.com/rbryanben/Nzungu"> Nzungu </a>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .card {
        padding: 30px 20px;
        top: 40%;
        min-width: 280px;
    }
    .input-wrapper {
        margin-top: 15px;
    }

    .button-wrapper {
        margin-top: 20px;
    }

    .legend {
        margin-top: 30px;
        text-align: center;
        font-size: small;
    }
</style>

<script>
    import TitledInput from "../components/TitledInput";
    import PlainButton from "../components/PlainButton";
    import validators from "../shared/validators"
    import { r_authenticate } from "@/repo/AuthorizationRepo";
import { notify_failed } from "@/utils/notifications";
import { handleAxiosError } from "@/utils/common";

    export default {
        name: 'LoginView',
        components: {
            TitledInput,
            PlainButton
        },
        data(){
            return {
                submitting: false,
                credentials : {
                    username: "",
                    password: ""
                }
            }
        },
        computed: {
            formValid(){
                return validators.username(this.credentials.username) && validators.password(this.credentials.password)
            },
            disableSubmit(){
                return this.submitting || !this.formValid
            }
        },
        methods: {
            onLoginResult(success,payload){

                // Failed login
                if (!success){
                    
                    // stop submitting 
                    this.submitting = false

                    // handle common error 
                    handleAxiosError(payload,{
                        onUnauthorized: (err)=>{
                            notify_failed('Invalid username or password')
                        }
                    })

                    return
                }

                // Success then write authorization token to local storage 
                localStorage.setItem('authorization',payload.token)
                this.$router.replace({ name: 'sales' });
            },
            onLoginClicked(e){
                // Start submiting
                this.submitting = true

                // sign in 
                r_authenticate(this.credentials,this.onLoginResult)
            },
            formChange(key,e){
                this.credentials[key] = e
            }
        }
    }
</script>