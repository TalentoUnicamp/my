<template>
    <div>
        <br>
        <div>
            <h2 class="ui header centered">
                <div class="content">
                    Participantes
                    <div class="sub header">Aqui estão todas as estatísticas que representam os participantes atuais</div>
                </div>
            </h2>
        </div>
        <br>
        <div class="ui container center aligned">
            <sui-statistic size="huge">
                <sui-statistic-value>{{ stats.hackers }}</sui-statistic-value>
                <sui-statistic-label>Participantes totais</sui-statistic-label>
            </sui-statistic>

            <br>
            <sui-statistics-group :columns="3">
                <sui-statistic in-group>
                    <sui-statistic-value>{{ stats.checked_in }}</sui-statistic-value>
                    <sui-statistic-label>Fizeram check-in</sui-statistic-label>
                </sui-statistic>
                <sui-statistic in-group>
                    <sui-statistic-value>{{ stats.confirmed }}</sui-statistic-value>
                    <sui-statistic-label>Confirmados</sui-statistic-label>
                </sui-statistic>
                <sui-statistic in-group>
                    <sui-statistic-value>{{ stats.admitted }}</sui-statistic-value>
                    <sui-statistic-label>Admitidos</sui-statistic-label>
                </sui-statistic>
            </sui-statistics-group>
            <br>
            <sui-statistics-group :columns="3">
                <sui-statistic in-group>
                    <sui-statistic-value>{{ stats.withdraw }}</sui-statistic-value>
                    <sui-statistic-label>Desistiram</sui-statistic-label>
                </sui-statistic>
                <sui-statistic in-group>
                    <sui-statistic-value>{{ stats.declined }}</sui-statistic-value>
                    <sui-statistic-label>Recusados</sui-statistic-label>
                </sui-statistic>
                <sui-statistic in-group>
                    <sui-statistic-value>{{ stats.waitlist }}</sui-statistic-value>
                    <sui-statistic-label>Fila de espera</sui-statistic-label>
                </sui-statistic>
            </sui-statistics-group>
            <br>
            <sui-statistics-group :columns="3">
                <sui-statistic in-group>
                    <sui-statistic-value>{{ stats.late }}</sui-statistic-value>
                    <sui-statistic-label>Atrasados</sui-statistic-label>
                </sui-statistic>
                <sui-statistic in-group>
                    <sui-statistic-value>{{ stats.incomplete }}</sui-statistic-value>
                    <sui-statistic-label>Incompletos</sui-statistic-label>
                </sui-statistic>
                <sui-statistic in-group>
                    <sui-statistic-value>{{ stats.unverified }}</sui-statistic-value>
                    <sui-statistic-label>Não verificados</sui-statistic-label>
                </sui-statistic>
            </sui-statistics-group>
        </div>
    </div>
</template>
<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";

export default {
    props: ["stats_context"],
    data() {
        return {
            stats: this.stats_context
        };
    },
    methods: {
        getHackerStats() {
            self = this;
            axios
                .get(this.stats.api.hacker_stats)
                .then(function(data) {
                    self.stats = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        }
    },
    mounted: function() {
        this.getHackerStats();
    }
};
</script>
