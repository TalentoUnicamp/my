<template>
    <div>
        <sui-divider />
        <br>
        <div class="header divided title">
            Avisos importantes
        </div>
        <sui-list id="info_list">
            <sui-list-item>O evento começa {{ event_start }} e vai até {{ event_end }}</sui-list-item>
            <sui-list-item><b>O período de check-in é das 9:00 às 19:00, {{ event_start_day }}.</b> Não aceitaremos participantes após esse horário</sui-list-item>
            <!-- <sui-list-item><b>Se informe!</b> Leia as <a target="_blank" href="">regras do evento e os critérios de avaliação!</a></sui-list-item> -->
            <sui-list-item>
                Precisa de mais informações? <a target="_blank" href="https://mte.org.br/contato/">Fale conosco</a>!
            </sui-list-item>
        </sui-list>
        <br>
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
        props: ['settings_context'],
        data() {
            return {
                settings: this.settings_context,
            }
        },
        computed: {
            event_start() {
                return moment(this.settings.hackathon_start_seconds).calendar();
            },
            event_start_day() {
                return moment(this.settings.hackathon_start_seconds).calendar(null, {
                    sameDay: '[Hoje]',
                    nextDay: '[Amanhã]',
                    nextWeek: 'dddd',
                    lastDay: '[Ontem]',
                    lastWeek: '[Última] dddd',
                    sameElse: 'DD/MM/YYYY'
                });
            },
            event_end() {
                return moment(this.settings.hackathon_end_seconds).calendar();
            }
        }
    }
</script>

<style scoped>
#info_list {
    text-align: left;
}
</style>
