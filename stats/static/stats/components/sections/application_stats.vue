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
        <br>
        <br>
        <div class="divided title">Informações Básicas</div>
        <br>
        <div class="ui stackable two column centered grid">
            <div class="row">
                <div class="column">
                    <component
                    v-bind:is="chartType"
                    :title="'Gênero'"
                    :values="genderList.items"
                    :labels="genderList.labels" />
                </div>
                <div class="column">
                    <component
                    v-bind:is="chartType"
                    :title="'Idades (top 10)'"
                    :values="ageList.items"
                    :labels="ageList.labels" />
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
                    <component
                    v-bind:is="chartType"
                    :title="'Níveis de educação'"
                    :values="educationList.items"
                    :labels="educationList.labels" />
                </div>
                <div class="column">
                    <component
                    v-bind:is="chartType"
                    :title="'Ano de ingresso (top 10)'"
                    :values="enrollYearList.items"
                    :labels="enrollYearList.labels" />
                </div>
            </div>
            <div class="row">
                <div class="column">
                    <component
                    v-bind:is="chartType"
                    :title="'Faculdades (top 10)'"
                    :values="schoolList.items"
                    :labels="schoolList.labels" />
                </div>
                <div class="column">
                    <component
                    v-bind:is="chartType"
                    :title="'Cursos (top 10)'"
                    :values="courseList.items"
                    :labels="courseList.labels" />
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
                    <component
                    v-bind:is="chartType"
                    :title="'País (top 10)'"
                    :values="countryList.items"
                    :labels="countryList.labels" />
                </div>
                <div class="column">
                    <component
                    v-bind:is="chartType"
                    :title="'Pode se mudar para trabalhar'"
                    :values="canMoveList.items"
                    :labels="canMoveList.labels" />
                </div>
            </div>
            <div class="row">
                <div class="column">
                    <component
                    v-bind:is="chartType"
                    :title="'Nível de inglês'"
                    :values="englishList.items"
                    :labels="englishList.labels" />
                </div>
                <div class="column">
                    <component
                    v-bind:is="chartType"
                    :title="'Nível de excel'"
                    :values="excelList.items"
                    :labels="excelList.labels" />
                </div>
            </div>
        </div>
        <br>
        <br>
        <sui-divider />
        <br>
        <div class="divided title">Talento</div>
        <p style="text-align: center;">Obs: Valores nulos representam participantes que não preencheram o campo específico</p>
        <br>
        <div class="ui stackable two column centered grid">
            <div class="row">
                <div class="column">
                    <component
                    v-bind:is="chartType"
                    :title="'Primeira vez na Talento'"
                    :values="firstTimerList.items"
                    :labels="firstTimerList.labels" />
                </div>
                <div class="column middle aligned" style="text-align: center;">
                    <h3 class="ui header">Referrer para o evento (top 10)</h3>
                    <sui-label v-for="referrer in referrerWordVector" v-bind:key="referrer[0]" color="blue">
                        {{ referrer[0] }}<sui-label-detail>{{ referrer[1] }}</sui-label-detail>
                    </sui-label>
                </div>
            </div>
        </div>
        <br>
        <br>
        <sui-divider />
        <br>
        <div class="divided title">Análises textuais</div>
        <br>
        <div class="ui stackable two column centered grid">
            <div class="row">
                <div class="column" style="text-align: center;">
                    <h3 class="ui header">Empresas dos sonhos (top 10)</h3>
                    <sui-label v-for="company in dreamCompanyWordVector" v-bind:key="company[0]" color="blue">
                        {{ company[0] }}<sui-label-detail>{{ company[1] }}</sui-label-detail>
                    </sui-label>
                </div>
                <div class="column" style="text-align: center;">
                    <h3 class="ui header">Interesses (top 10)</h3>
                    <sui-label v-for="interest in interestsWordVector" v-bind:key="interest[0]" color="green">
                        {{ interest[0] }}<sui-label-detail>{{ interest[1] }}</sui-label-detail>
                    </sui-label>
                </div>
            </div>
            <div class="row">
                <div class="column" style="text-align: center;">
                    <h3 class="ui header">Cursos extras (top 10)</h3>
                    <sui-label v-for="course in extraCoursesWordVector" v-bind:key="course[0]" color="red">
                        {{ course[0] }}<sui-label-detail>{{ course[1] }}</sui-label-detail>
                    </sui-label>
                </div>
                <div class="column" style="text-align: center;">
                    <h3 class="ui header">Línguas faladas (top 10)</h3>
                    <sui-label v-for="language in languagesWordVector" v-bind:key="language[0]" color="cyan">
                        {{ language[0] }}<sui-label-detail>{{ language[1] }}</sui-label-detail>
                    </sui-label>
                </div>
            </div>
            <div class="row">
                <div class="column" style="text-align: center;">
                    <h3 class="ui header">Horários disponíveis (top 10)</h3>
                    <sui-label v-for="slot in timeSlotsWordVector" v-bind:key="slot[0]" color="orange">
                        {{ slot[0] }}<sui-label-detail>{{ slot[1] }}</sui-label-detail>
                    </sui-label>
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

import plotlyBar from "stats/components/plotlyCharts/simpleBar.vue";

import nlp from "project/mixins/nlp.vue";

export default {
    props: ["stats_context"],
    components: { simplePie, plotlyBar },
    mixins: [nlp],
    data() {
        return {
            stats: this.stats_context,
            applicationList: [],
            chartType: "plotly-bar",
            chartTypes: [
                { key: "bar", value: "plotly-bar", text: "Barras" },
                { key: "pie", value: "simple-pie", text: "Pizza" }
            ]
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
            if (sort == "asc")
                res.sort((a1, a2) => {
                    return a1[1].length - a2[1].length;
                });
            if (sort == "desc")
                res.sort((a1, a2) => {
                    return a2[1].length - a1[1].length;
                });
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
                "desc"
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
                "desc"
            );
            res.labels = res.labels.slice(0, 10);
            res.items = res.items.slice(0, 10);
            return res;
        },
        schoolList() {
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.school,
                "desc"
            );
            res.labels = res.labels.slice(0, 10);
            res.items = res.items.slice(0, 10);
            return res;
        },
        courseList() {
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.course,
                "desc"
            );
            res.labels = res.labels.slice(0, 10);
            res.items = res.items.slice(0, 10);
            return res;
        },
        countryList() {
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.country,
                "desc"
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
                if (label) return labelMap[label];
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
                if (label) return labelMap[label];
                return "Não respondeu";
            });
            return res;
        },
        firstTimerList() {
            let labelMap = {
                true: "Sim",
                false: "Não",
                null: "Não",
                undefined: "Não"
            };
            let res = this.groupByLabelsLen(
                this.applicationList,
                app => app.application.first_timer
            );
            res.labels = res.labels.map(label => {
                if (label) return labelMap[label];
                return "Não";
            });
            return res;
        },
        dreamCompanyWordVector() {
            let companies = this.applicationList
                .map(app => app.application.dream_company)
                .filter(company => company).map(company => company.toLowerCase());
            let companiesCV = this.countVectorizeArray(companies);
            let companiesCVArr = Object.entries(companiesCV);
            companiesCVArr.sort((company1, company2) => company2[1] - company1[1]);
            return companiesCVArr.slice(0, 10);
        },
        interestsWordVector() {
            let interests = this.flatten(
                this.applicationList.map(app =>
                    app.application.interests
                        .split(",")
                        .map(interest => interest.trim())
                )
            ).filter(interest => interest).map(interest => interest.toLowerCase());
            let interestsCV = this.countVectorizeArray(interests);
            let interestsCVArr = Object.entries(interestsCV);
            interestsCVArr.sort((interest1, interest2) => interest2[1] - interest1[1]);
            return interestsCVArr.slice(0, 10);
        },
        extraCoursesWordVector() {
            let courses = this.flatten(
                this.applicationList.map(app =>
                    app.application.extra_courses).filter(course => course).map(course => course.split(','))
            ).map(course => course.toLowerCase().trim());
            let coursesCV = this.countVectorizeArray(courses);
            let coursesCVArr = Object.entries(coursesCV);
            coursesCVArr.sort((course1, course2) => course2[1] - course1[1]);
            return coursesCVArr.slice(0, 10);
        },
        languagesWordVector() {
            let languages = this.flatten(
                this.applicationList.map(app =>
                    app.application.other_languages).filter(language => language).map(language => language.split(','))
            ).map(language => language.toLowerCase().trim());
            let languagesCV = this.countVectorizeArray(languages);
            let languagesCVArr = Object.entries(languagesCV);
            languagesCVArr.sort((language1, language2) => language2[1] - language1[1]);
            return languagesCVArr.slice(0, 10);
        },
        timeSlotsWordVector() {
            let slots = this.flatten(
                this.applicationList.map(app =>
                    app.application.time_slots).filter(slot => slot).map(slot => slot.split(','))
            ).map(slot => slot.toLowerCase().trim());
            let slotsCV = this.countVectorizeArray(slots);
            let slotsCVArr = Object.entries(slotsCV);
            slotsCVArr.sort((slot1, slot2) => slot2[1] - slot1[1]);
            return slotsCVArr.slice(0, 10);
        },
        referrerWordVector() {
            let referrer = this.flatten(
                this.applicationList.map(app =>
                    app.application.referrer).filter(referrer => referrer).map(referrer => referrer.split(','))
            ).map(referrer => referrer.toLowerCase().trim());
            let referrerCV = this.countVectorizeArray(referrer);
            let referrerCVArr = Object.entries(referrerCV);
            referrerCVArr.sort((referrer1, referrer2) => referrer2[1] - referrer1[1]);
            return referrerCVArr.slice(0, 10);
        }
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
.ui .label {
    margin-bottom: 5px;
}
</style>
