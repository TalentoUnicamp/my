<template>
    <div>
        <sui-divider />
        <br>
        <div class="header divided title">
            Acesso
        </div>
        <div class="description">
            Não corra o risco de perder sua conta. Associe outros serviços e guarde seu token em um local seguro.
        </div>
        <p>
            <div class="header">Acesso por Token</div>
            <code>Seu Token: {{ user.token }}</code>
            <br>
            <sui-button size="small" color="red" @click="changeToken" content="Trocar Token" />
        </p>
        <p>
            <div class="header">Acesso pelo Facebook</div>
            <sui-button :loading="loadingSocial.facebook" :disabled="loadingSocial.facebook" social="facebook" v-bind:content="fb_text" @click="fbLogin" />
        </p>
        <p>
            <div class="header">Acesso pelo GitHub</div>
            <sui-button :loading="loadingSocial.github" :disabled="loadingSocial.github" color="black" v-bind:content="gh_text" @click="ghLogin" />
        </p>
        <p>
            <div class="header">Acesso pelo Google</div>
            <sui-button :loading="loadingSocial.google" :disabled="loadingSocial.google" social="youtube" v-bind:content="go_text" @click="goLogin" />
        </p>
        <br>
    </div>
</template>

<script>
    import axios from 'project/js/axios_csrf';
    import toast from 'project/js/notifications';

    export default {
        props: ['user_context', 'dashboard_context'],
        data() {
            return {
                user: this.user_context,
                dashboard: this.dashboard_context,
                has_facebook: this.user_context.social.has_facebook,
                has_github: this.user_context.social.has_github,
                has_google: this.user_context.social.has_google,
                loadingSocial: {
                    facebook: false,
                    github: false,
                    google: false
                }
            }
        },
        computed: {
            fb_text: function() {
                if (this.has_facebook) {
                    return 'Desvincular Facebook';
                }
                return 'Vincular Facebook';
            },
            gh_text: function () {
                if (this.has_github) {
                    return 'Desvincular Github';
                }
                return 'Vincular Github';
            },
            go_text: function () {
                if (this.has_google) {
                    return 'Desvincular Google';
                }
                return 'Vincular Google';
            },
        },
        methods: {
            changeToken() {
                self = this;
                axios.post(this.dashboard.api.change_token)
                .then(function (data) {
                    self.user.token = data.data.token;
                    toast('Sucesso', 'Token alterado :)', 'success');
                })
                .catch(function (error) {
                    console.log(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            },
            fbLogin() {
                if (this.has_facebook) {
                    this.unlink_social('facebook');
                    this.has_facebook = false;
                }
                else {
                    this.loadingSocial.facebook = true;
                    window.location.href = this.dashboard.social_urls.facebook;
                }
            },
            ghLogin() {
                if (this.has_github) {
                    this.unlink_social('github');
                    this.has_github = false;
                }
                else {
                    this.loadingSocial.github = true;
                    window.location.href = this.dashboard.social_urls.github;
                }
            },
            goLogin() {
                if (this.has_google) {
                    this.unlink_social('google');
                    this.has_google = false;
                }
                else {
                    this.loadingSocial.google = true;
                    window.location.href = this.dashboard.social_urls.google;
                }
            },
            unlink_social(provider) {
                axios.post(this.dashboard.api.unlink_provider, {
                    provider: provider
                })
                .then(function(data) {
                    toast('Desvinculado', 'Seu ' + provider + ' foi desvinculado', 'info');
                })
                .catch(function(error) {
                    console.log(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            }
        }
    }
</script>
