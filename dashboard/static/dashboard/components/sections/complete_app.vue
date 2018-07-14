<template>
    <div>
        <div class="description">
            <b>Atenção!</b> Você tem até {{ reg_date }} pra completar sua aplicação.
        </div>
        <sui-button primary @click="redirectApplication()" content="Complete sua aplicação" />
    </div>
</template>

<script>
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
        props: ['settings_context', 'sidebar_context'],
        data() {
            return {
                settings: this.settings_context,
                sidebar: this.sidebar_context
            }
        },
        computed: {
            reg_date() {
                return moment(this.settings.registration_close_seconds).calendar();
            }
        },
        methods: {
            redirectApplication() {
                window.location.href = this.sidebar.redirect_urls.application;
            }
        }
    }
</script>
