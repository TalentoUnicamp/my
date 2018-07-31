<template>
    <div>
        <sui-divider />
        <br>
        <div class="header divided title">
            Não poderá participar?
        </div>
        <div class="description">
            <b>Nos avise!</b> Assim poderemos cancelar sua inscrição e liberar a vaga para outra pessoa :)
            <br>
            Você ainda pode mudar de ideia até {{ conf_close }}.
        </div>
        <br>
        <sui-button primary @click="withdraw()" content="Desculpe, não vou conseguir" />
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
                conf_close_raw: this.settings_context.confirmation_seconds
            }
        },
        computed: {
            conf_close() {
                return moment(this.conf_close_raw).calendar();
            }
        },
        methods: {
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
