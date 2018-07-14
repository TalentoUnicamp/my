<template>
    <div>
        <sui-divider />
        <br>
        <p>
            Enviamos um email de confirmação para {{ sentEmail }}. Use-o para completar sua inscrição.
        </p>
        <p v-if="user.is_hacker">
            <b>Você tem até {{ reg_close }} para fazer isso</b>
        </p>
        <p>
            Não recebeu ou não é o seu email?
        </p>
        <sui-form @submit.prevent="resendEmail()">
            <sui-form-field>
                <p v-if="errors.length">
                    {{ errors }}
                </p>
                <sui-input type="email" v-bind:loading="emailLoading" v-bind:disabled="emailLoading" v-model="user.email" placeholder="Digite seu email" required />
            </sui-form-field>
            <sui-form-field>
                <sui-button v-bind:loading="emailLoading" v-bind:disabled="emailLoading" color="red" content="Reenviar email" />
            </sui-form-field>
        </sui-form>
        <br>
    </div>
</template>

<script>
    import axios from 'project/js/axios_csrf';
    import toast from 'project/js/notifications';
    import * as mome from 'moment';
    import 'moment/locale/pt-br';

    if ("default" in mome) {
        var moment = mome["default"];
    }
    else {
        var moment = mome;
    }

    moment.locale('pt-BR');

    export default {
        props: ['user_context', 'settings_context', 'dashboard_context'],
        data() {
            return {
                errors: '',
                user: this.user_context,
                settings: this.settings_context,
                dashboard: this.dashboard_context,
                sentEmail: this.user_context.email,
                emailLoading: false,
                reg_close_raw: this.settings_context.registration_close_seconds
            }
        },
        computed: {
            reg_close() {
                return moment(this.reg_close_raw).calendar();
            }
        },
        methods: {
            resendEmail() {
                if (!this.user.email) {
                    this.errors = 'Email necessário';
                    return;
                }
                if (!this.validEmail(this.user.email)) {
                    this.errors = 'Email inválido';
                    return;
                }
                this.errors = '';
                this.emailLoading = true;
                self = this;
                axios.post(this.dashboard.api.change_email, {
                    email: self.user.email
                })
                .then(function (data) {
                    toast('Enviado', data.data.message, 'success');
                    self.sentEmail = self.user.email;
                })
                .catch(function (error) {
                    console.log(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                })
                .then(function () {
                    self.emailLoading = false;
                })
            },
            validEmail: function (email) {
              var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
              return re.test(email);
          }
      }
  }
</script>
