<template>
    <div id="login">
        <sui-container>
            <div class="content">
                <sui-segment>
                    <div class="logo">
                        <img v-bind:src="context.event_logo_text">
                    </div>
                    <sui-divider horizontal></sui-divider>
                    <div v-if="loginState === 'login'">
                        <sui-form @submit.prevent="tokenLogin()" v-bind:error="error">
                            <sui-form-field>
                                <sui-message error>
                                    {{ errorMessage }}
                                </sui-message>
                                <label>Token</label>
                                <sui-input v-bind:loading="tokenLoading" v-bind:disabled="tokenLoading" type="text" required placeholder="AbC123" v-model="token"/>
                            </sui-form-field>
                            <sui-button v-bind:loading="tokenLoading" v-bind:disabled="tokenLoading" className='login' fluid content='Entrar com token' type="submit" />
                        </sui-form>
                        <sui-form :loading="formLoading">
                            <sui-divider horizontal>Ou</sui-divider>
                            <sui-form-field>
                                <sui-button type="button" @click="socialLogin('facebook')" fluid social="facebook" content="Entrar com Facebook" icon="facebook"/>
                            </sui-form-field>
                            <sui-form-field>
                                <sui-button type="button" @click="socialLogin('github')" fluid color="black" content="Entrar com GitHub" icon="github"/>
                            </sui-form-field>
                            <sui-form-field>
                                <sui-button type="button" @click="socialLogin('google')" fluid social="youtube" content="Entrar com Google" icon="google"/>
                            </sui-form-field>
                        </sui-form>
                    </div>
                    <div v-if="loginState === 'forgot'">
                        <div class="ui forgot-password form">
                            <sui-form v-bind:success="success" @submit.prevent="sendResetEmail()">
                                <sui-message success>
                                    {{ successMessage }}
                                </sui-message>
                                <sui-form-field>
                                    <label> Email</label>
                                    <sui-input type="email" v-bind:loading="emailLoading" v-bind:disabled="emailLoading" required placeholder="foo@bar.com" v-model="resetEmail"/>
                                </sui-form-field>
                                <sui-form-field>
                                    <sui-button v-bind:loading="emailLoading" v-bind:disabled="emailLoading" className='login' fluid content='Recuperar token' type="submit" />
                                </sui-form-field>
                            </sui-form>
                        </div>
                    </div>

                    <div class="ui divider"></div>

                    <div v-if="loginState === 'login'" class="forgot">
                        <a href="#" @click="setLoginState('forgot')">
                            Esqueceu seu token?
                        </a>
                    </div>
                    <div v-if="loginState === 'forgot'" class="forgot">
                        <a href="#" @click="setLoginState('login')">
                            Fazer login
                        </a>
                    </div>
                </sui-segment>
            </div>
        </sui-container>
    </div>
</template>
<script>
import axios from "axios";

export default {
    props: ["login_context"],
    data() {
        return {
            errorMessage: login_context.error != "" ? login_context.error : "",
            successMessage: "",
            loginState: "login",
            tokenLoading: false,
            emailLoading: false,
            formLoading: false,
            resetEmail: "",
            token: "",
            context: login_context
        };
    },
    computed: {
        error: function() {
            return this.errorMessage != "" ? true : false;
        },
        success: function() {
            return this.successMessage != "" ? true : false;
        }
    },
    methods: {
        setLoginState(state) {
            this.loginState = state;
        },
        tokenLogin() {
            self.errorMessage = "";
            if (this.token === "") return;
            self = this;
            this.tokenLoading = true;
            axios
                .post(this.context.check_token_url, {
                    token: this.token
                })
                .then(function(response) {
                    window.location.href = response.data.redirect_url;
                })
                .catch(function(error) {
                    self.errorMessage = error.response.data.error;
                    self.tokenLoading = false;
                });
        },
        sendResetEmail() {
            if (this.resetEmail === "") return;
            self = this;
            this.emailLoading = true;
            axios
                .post(this.context.reset_email_url, {
                    email: self.resetEmail
                })
                .then(function(response) {
                    self.successMessage = response.data.message;
                })
                .catch(function(error) {
                    console.error(error);
                })
                .then(function() {
                    self.emailLoading = false;
                });
        },
        socialLogin(login) {
            this.formLoading = true;
            if (login === "facebook") {
                window.location.pathname = this.context.social_urls.facebook;
            }
            if (login === "github") {
                window.location.pathname = this.context.social_urls.github;
            }
            if (login === "google") {
                window.location.pathname = this.context.social_urls.google;
            }
        }
    }
};
</script>
