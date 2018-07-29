<template>
    <div>
        <br>
        <div>
            <h2 class="ui header centered">
                <div class="content">
                    Aplicações
                    <div class="sub header">Aqui estão estatísticas que representam as aplicações enviadas pelos participantes</div>
                </div>
            </h2>
        </div>
        <br>
        <br>
        <div class="divided title">Informações Básicas</div>
        <br>
        <div class="ui stackable two column centered grid">
            <div class="row">
                <div class="column">
                    <simple-pie
                    :data_points="genderList.items"
                    :labels="genderList.labels"
                    :chart-id="'gender'"
                    :options="{
                        responsive: true,
                        maintainAspectRatio: false,
                        title: {
                            display: true,
                            text: 'Gênero'
                        }
                    }"/>
                </div>
                <div class="column">
                    <simple-pie
                    :data_points="ageList.items"
                    :labels="ageList.labels"
                    :chart-id="'age'"
                    :options="{
                        responsive: true,
                        maintainAspectRatio: false,
                        title: {
                            display: true,
                            text: 'Idades (top 10)'
                        }
                    }"/>
                </div>
            </div>
        </div>
        <br>
        <br>
        <sui-divider />
        <br>
        <div class="divided title">Educação</div>
        <p style="text-align: center;">Obs: Valores nulos representam participantes que não preencheram o campo específico</p>
        <br>
        <div class="ui stackable two column centered grid">
            <div class="row">
                <div class="column">
                    <simple-pie
                    :data_points="educationList.items"
                    :labels="educationList.labels"
                    :chart-id="'education'"
                    :options="{
                        responsive: true,
                        maintainAspectRatio: false,
                        title: {
                            display: true,
                            text: 'Níveis de educação'
                        }
                    }"/>
                </div>
                <div class="column">
                    <simple-pie
                    :data_points="enrollYearList.items"
                    :labels="enrollYearList.labels"
                    :chart-id="'enroll_year'"
                    :options="{
                        responsive: true,
                        maintainAspectRatio: false,
                        title: {
                            display: true,
                            text: 'Ano de ingresso (top 10)'
                        }
                    }"/>
                </div>
            </div>
            <div class="row">
                <div class="column">
                    <simple-pie
                    :data_points="schoolList.items"
                    :labels="schoolList.labels"
                    :chart-id="'school'"
                    :options="{
                        responsive: true,
                        maintainAspectRatio: false,
                        title: {
                            display: true,
                            text: 'Faculdades (top 10)'
                        }
                    }"/>
                </div>
                <div class="column">
                    <simple-pie
                    :data_points="courseList.items"
                    :labels="courseList.labels"
                    :chart-id="'course'"
                    :options="{
                        responsive: true,
                        maintainAspectRatio: false,
                        title: {
                            display: true,
                            text: 'Cursos (top 10)'
                        }
                    }"/>
                </div>
            </div>
        </div>
        <br>
        <br>
        <sui-divider />
        <br>
        <div class="divided title">Informações extras</div>
        <p style="text-align: center;">Obs: Valores nulos representam participantes que não preencheram o campo específico</p>
        <br>
        <div class="ui stackable two column centered grid">
            <div class="row">
                <div class="column">
                    <simple-pie
                    :data_points="countryList.items"
                    :labels="countryList.labels"
                    :chart-id="'country'"
                    :options="{
                        responsive: true,
                        maintainAspectRatio: false,
                        title: {
                            display: true,
                            text: 'País (top 10)'
                        }
                    }"/>
                </div>
                <div class="column">
                    <simple-pie
                    :data_points="canMoveList.items"
                    :labels="canMoveList.labels"
                    :chart-id="'can_move'"
                    :options="{
                        responsive: true,
                        maintainAspectRatio: false,
                        title: {
                            display: true,
                            text: 'Pode se mudar para trabalhar'
                        }
                    }"/>
                </div>
            </div>
            <div class="row">
                <div class="column">
                    <simple-pie
                    :data_points="englishList.items"
                    :labels="englishList.labels"
                    :chart-id="'english'"
                    :options="{
                        responsive: true,
                        maintainAspectRatio: false,
                        title: {
                            display: true,
                            text: 'Nível de inglês'
                        }
                    }"/>
                </div>
                <div class="column">
                    <simple-pie
                    :data_points="excelList.items"
                    :labels="excelList.labels"
                    :chart-id="'excel'"
                    :options="{
                        responsive: true,
                        maintainAspectRatio: false,
                        title: {
                            display: true,
                            text: 'Nível de excel'
                        }
                    }"/>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import moment from "project/js/moment";

import simplePie from "stats/components/charts/simplePie.vue";
import timeSeries from "stats/components/charts/timeSeries.vue";

export default {
    props: ["stats_context"],
    components: { simplePie, timeSeries },
    data() {
        return {
            stats: this.stats_context,
            applicationList: []
        };
    },
    methods: {
        getApplicationStats() {
            var comp = this;
            axios
                .get(this.stats.api.hacker_application_list)
                .then(function(data) {
                    comp.applicationList = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        groupBy(list, keyGetter, sort) {
            // groupBy(pets, pet => pet.type).get("Dog");
            const map = new Map();
            list.forEach(item => {
                const key = keyGetter(item);
                const collection = map.get(key);
                if (!collection) {
                    map.set(key, [item]);
                } else {
                    collection.push(item);
                }
            });
            let res = Array.from(map);
            if (sort == 'asc')
                res.sort((a1, a2) => {return a1[1].length - a2[1].length;});
            if (sort == 'desc')
                res.sort((a1, a2) => {return a2[1].length - a1[1].length;})
            return res;
        },
        groupByLabelsItems(data, key, sortFunc) {
            // Returns a grouped by labels and entities as
            // two separate lists
            // {labels: ["l1", "l2"], items: [[obj1, obj2], [obj3, obj4]]}
            let group = this.groupBy(data, key, sortFunc);
            let res = { labels: [], items: [] };
            for (let k in group) {
                res.labels.push(group[k][0]);
                res.items.push(group[k][1]);
            }
            return res;
        },
        groupByLabelsLen(data, key, sortFunc) {
            // Returns a grouped by labels and entities len
            // {labels: ["l1", "l2"], items: [2, 3]}
            let group = this.groupBy(data, key, sortFunc);
            let res = { labels: [], items: [] };
            for (let k in group) {
                res.labels.push(group[k][0]);
                res.items.push(group[k][1].length);
            }
            return res;
        }
    },
    computed: {
        bucketedApplicationList() {
            let buckets = [];
            let data = this.applicationList.map(d => {
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
        genderList() {
            let labelMap = {
                M: "Masculino",
                F: "Feminino",
                O: "Outro",
                NA: "Prefiro não dizer"
            };
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.gender
            );
            res.labels = res.labels.map(label => {
                return labelMap[label];
            });
            return res;
        },
        ageList() {
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.age,
                'desc'
            );
            res.labels = res.labels.slice(0, 10);
            res.items = res.items.slice(0, 10);
            return res;
        },
        educationList() {
            return this.groupByLabelsLen(
                this.applicationList,
                app => app.application.education
            );
        },
        enrollYearList() {
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.enroll_year,
                'desc'
            );
            res.labels = res.labels.slice(0, 10);
            res.items = res.items.slice(0, 10);
            return res;
        },
        schoolList() {
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.school,
                'desc'
            );
            res.labels = res.labels.slice(0, 10);
            res.items = res.items.slice(0, 10);
            return res;
        },
        courseList() {
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.course,
                'desc'
            );
            res.labels = res.labels.slice(0, 10);
            res.items = res.items.slice(0, 10);
            return res;
        },
        countryList() {
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.country,
                'desc'
            );
            res.labels = res.labels.slice(0, 10);
            res.items = res.items.slice(0, 10);
            return res;
        },
        canMoveList() {
            let labelMap = {
                true: "Sim",
                false: "Não",
                null: "Não respondeu",
                undefined: "Não respondeu"
            };
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.can_move
            );
            res.labels = res.labels.map(label => {
                return labelMap[label];
            });
            return res;
        },
        englishList() {
            let labelMap = {
                basic: "Básico",
                intermediate: "Intermediário",
                advanced: "Avançado",
                undefined: "Não respondeu"
            };
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.english_level
            );
            res.labels = res.labels.map(label => {
                if (label)
                    return labelMap[label]
                return "Não respondeu";
            });
            return res;
        },
        excelList() {
            let labelMap = {
                basic: "Básico",
                intermediate: "Intermediário",
                advanced: "Avançado",
                undefined: "Não respondeu"
            };
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.excel_level
            );
            res.labels = res.labels.map(label => {
                if (label)
                    return labelMap[label]
                return "Não respondeu";
            });
            return res;
        },
    },
    mounted: function() {
        this.getApplicationStats();
    }
};
</script>

<style scoped>
.page .title {
    font-size: 1em;
}
</style>
