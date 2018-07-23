<template>
    <div>
        <sui-divider />
        <br>
        <div class="header divided title">
            Confirmar presença
        </div>
        <div class="description">
            <b>Atenção!</b> Você ainda precisa confirmar sua presença até {{ conf_close }}
        <br>
        <br>
            <b>Não confirmar sua presença até esse dia significará a perda de seu lugar no evento!</b>
        </div>
        <sui-button color="blue" @click="confirm()" content="Confirmar presença" />
        <br>
        <br>
        <div class="description">
            Não vai poder participar? Nos avise!
        </div>
        <sui-button color="red" @click="withdraw()" content="Não posso participar" />
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
                user: this.user_context,
                settings: this.settings_context,
                dashboard: this.dashboard_context,
                reg_close_raw: this.settings_context.registration_close_seconds,
                conf_close_raw: this.settings_context.confirmation_seconds
            }
        },
        computed: {
            reg_close() {
                return moment(this.reg_close_raw).calendar();
            },
            conf_close() {
                return moment(this.conf_close_raw).calendar();
            }
        },
        methods: {
            confirm() {
                self = this;
                axios.post(this.dashboard.api.confirm)
                .then(function (data) {
                    toast('Sucesso!', data.data.message, 'success');
                    self.user.state = data.data.state;
                })
                .catch(function (error) {
                    console.log(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            },
            withdraw() {
                self = this;
                axios.post(this.dashboard.api.withdraw)
                .then(function (data) {
                    toast('Que pena :(', data.data.message, 'info');
                    self.user.state = data.data.state;
                })
                .catch(function (error) {
                    console.log(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            }
        }
    }
</script>
