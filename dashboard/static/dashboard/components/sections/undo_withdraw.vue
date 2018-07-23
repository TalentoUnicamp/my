<template>
    <div>
        <sui-divider />
        <br>
        <div class="header divided title">
            Mudar de ideia
        </div>
        <div class="description">
            <b>Você ainda tem até {{ conf_close }} para reativar sua aplicação!</b>
        </div>
        <br>
        <sui-button primary @click="undo_withdraw()" content="Mudei de ideia!" />
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
            undo_withdraw() {
                self = this;
                axios.post(this.dashboard.api.undo_withdraw)
                .then(function (data) {
                    toast('Ótimo!', data.data.message, 'success');
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
