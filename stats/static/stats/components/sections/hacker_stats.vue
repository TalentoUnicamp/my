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
        <plotly-area
        :values="bucketedSignupList2.y"
        :labels="bucketedSignupList2.x"
        :title="'Inscrição de participantes ao longo do tempo'" />
        <br>
        <br>
        <div class="ui stackable one column centered grid">
            <div class="column">
                <sui-form>
                    <sui-form-fields>
                        <sui-form-field>
                            <label>Tipo de gráfico</label>
                            <sui-dropdown
                            :options="chartTypes"
                            placeholder="Tipo de gráficos"
                            selection
                            v-model="chartType" />
                        </sui-form-field>
                    </sui-form-fields>
                </sui-form>
            </div>
        </div>
        <component
        v-bind:is="chartType"
        :values="statsList"
        :labels="statsLabels"
        :title="'Estado dos participantes'" />
        <br>
        <br>
        <div class="ui container center aligned">
            <sui-statistic>
                <sui-statistic-value>{{ hacker_stats.hackers }}</sui-statistic-value>
                <sui-statistic-label>Participantes totais</sui-statistic-label>
            </sui-statistic>

            <br>
            <sui-statistics-group :columns="4">
                <sui-statistic size="small" in-group>
                    <sui-statistic-value>{{ hacker_stats.checked_in }}</sui-statistic-value>
                    <sui-statistic-label>Fizeram check-in</sui-statistic-label>
                </sui-statistic>
                <sui-statistic size="small" in-group>
                    <sui-statistic-value>{{ hacker_stats.confirmed }}</sui-statistic-value>
                    <sui-statistic-label>Confirmados</sui-statistic-label>
                </sui-statistic>
                <sui-statistic size="small" in-group>
                    <sui-statistic-value>{{ hacker_stats.admitted }}</sui-statistic-value>
                    <sui-statistic-label>Admitidos</sui-statistic-label>
                </sui-statistic>
                <sui-statistic size="small" in-group>
                    <sui-statistic-value>{{ hacker_stats.submitted }}</sui-statistic-value>
                    <sui-statistic-label>Submetidos</sui-statistic-label>
                </sui-statistic>
            </sui-statistics-group>
            <br>
            <sui-statistics-group :columns="3">
                <sui-statistic size="small" in-group>
                    <sui-statistic-value>{{ hacker_stats.withdraw }}</sui-statistic-value>
                    <sui-statistic-label>Desistiram</sui-statistic-label>
                </sui-statistic>
                <sui-statistic size="small" in-group>
                    <sui-statistic-value>{{ hacker_stats.declined }}</sui-statistic-value>
                    <sui-statistic-label>Recusados</sui-statistic-label>
                </sui-statistic>
                <sui-statistic size="small" in-group>
                    <sui-statistic-value>{{ hacker_stats.waitlist }}</sui-statistic-value>
                    <sui-statistic-label>Fila de espera</sui-statistic-label>
                </sui-statistic>
            </sui-statistics-group>
            <br>
            <sui-statistics-group :columns="3">
                <sui-statistic size="small" in-group>
                    <sui-statistic-value>{{ hacker_stats.late }}</sui-statistic-value>
                    <sui-statistic-label>Atrasados</sui-statistic-label>
                </sui-statistic>
                <sui-statistic size="small" in-group>
                    <sui-statistic-value>{{ hacker_stats.incomplete }}</sui-statistic-value>
                    <sui-statistic-label>Incompletos</sui-statistic-label>
                </sui-statistic>
                <sui-statistic size="small" in-group>
                    <sui-statistic-value>{{ hacker_stats.unverified }}</sui-statistic-value>
                    <sui-statistic-label>Não verificados</sui-statistic-label>
                </sui-statistic>
            </sui-statistics-group>
        </div>
    </div>
</template>
<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import moment from "project/js/moment";

import plotlyArea from "stats/components/plotlyCharts/simpleArea.vue";
import plotlyBar from "stats/components/plotlyCharts/simpleBar.vue";
import simplePie from "stats/components/charts/simplePie.vue";

export default {
    props: ["stats_context"],
    components: { plotlyArea, plotlyBar, simplePie },
    data() {
        return {
            stats: this.stats_context,
            hacker_stats: {},
            signupList: [],
            bucketSize: 1,
            chartType: "plotly-bar",
            chartTypes: [
                { key: "bar", value: "plotly-bar", text: "Barras" },
                { key: "pie", value: "simple-pie", text: "Pizza" }
            ]
        };
    },
    methods: {
        getHackerStats() {
            var comp = this;
            axios
                .get(this.stats.api.hacker_stats)
                .then(function(data) {
                    comp.hacker_stats = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        getHackerSignupDates() {
            var comp = this;
            axios
                .get(this.stats.api.hacker_signup_list)
                .then(function(data) {
                    comp.signupList = data.data.map(date => {
                        return date.date_joined;
                    });
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        }
    },
    computed: {
        statsList() {
            return [
                this.hacker_stats.checked_in,
                this.hacker_stats.confirmed,
                this.hacker_stats.admitted,
                this.hacker_stats.submitted,
                this.hacker_stats.withdraw,
                this.hacker_stats.declined,
                this.hacker_stats.waitlist,
                this.hacker_stats.late,
                this.hacker_stats.incomplete,
                this.hacker_stats.unverified
            ];
        },
        statsLabels() {
            return [
                "Check-in",
                "Confirmados",
                "Admitidos",
                "Submetidos",
                "Desistiram",
                "Recusados",
                "Fila de espera",
                "Atrasados",
                "Incompletos",
                "Não verificados"
            ];
        },
        bucketedSignupList() {
            let buckets = [];
            let data = this.signupList.map(d => {
                return moment(d);
            });
            if (data.length == 0) return [];
            // Set first bucket
            let currentBucket = { x: data[0].toDate(), y: 0 };
            // For each date in data
            for (let i = 0; i < data.length; i++) {
                let date = data[i];
                // If on the current bucket, increase bucket size
                if (date.date() == currentBucket.x.getDate()) {
                    currentBucket.y++;
                } else {
                    buckets.push(currentBucket);
                    currentBucket = { x: date.toDate(), y: 1 };
                }
            }
            buckets.push(currentBucket);

            return buckets;
        },
        bucketedSignupList2() {
            let buckets = {
                x: [],
                y: [],
                type: "scatter",
                mode: "lines",
                fill: "tozeroy",
                name: "Teste",
                line: { shape: "spline", smoothing: 1 }
            };
            let data = this.signupList.map(d => {
                return moment(d).hours(0);
            });
            if (data.length == 0) return [];
            // Set first bucket
            let currentBucketx = data[0].toDate(),
                currentBuckety = 0;
            // For each date in data
            for (let i = 0; i < data.length; i++) {
                let date = data[i];
                // If on the current bucket, increase bucket size
                if (date.date() == currentBucketx.getDate()) {
                    currentBuckety++;
                } else {
                    buckets.x.push(currentBucketx);
                    buckets.y.push(currentBuckety);
                    currentBucketx = date.toDate();
                    currentBuckety = 1;
                }
            }
            buckets.x.push(currentBucketx);
            buckets.y.push(currentBuckety);

            return buckets;
        }
    },
    mounted: function() {
        this.getHackerStats();
        this.getHackerSignupDates();
    }
};
</script>
<style>
.ui.form .fields > .field:first-child {
    margin: auto;
}
</style>
