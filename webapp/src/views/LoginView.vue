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
                <TitledInput title="Username" validator="username"  v-on:on-text-changed="(e)=>{formChange('username',e)}" placeholder="Type your username"/>
            </div>
            <!-- Password -->
            <div class="input-wrapper">
                <TitledInput  title="Password" validator="password" v-on:on-text-changed="(e)=>{formChange('password',e)}" type="password" placeholder="Type your password"/>
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
            onLoginClicked(e){
                this.submitting = true
            },
            formChange(key,e){
                this.credentials[key] = e
            }
        }
    }
</script>