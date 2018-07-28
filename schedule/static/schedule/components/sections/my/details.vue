<template>
    <div>
        <sui-button icon="arrow left" content="Voltar" color="blue" @click="$emit('go-back')" />
        <br>
        <div>
            <h2 class="ui header centered">
                <div class="content">
                    {{ event.name }}
                </div>
            </h2>
        </div>
        <br>
        <div v-if="event.require_register" class="ui container center aligned">
            <sui-statistic size="huge" :color="rateColor">
                <sui-statistic-value>{{ rateText }}</sui-statistic-value>
                <sui-statistic-label>
                    Avaliação média <i class="ui question circle icon" data-html="Já que a distribuição de notas como essa tende a não ser muito uniforme, foi aplicada uma tranformação chamada <b>Laplace Smoothing</b>. Com ela, toda a distribuição é representada de forma menos tendenciosa"></i>
                </sui-statistic-label>
            </sui-statistic>
            <sui-statistics-group columns="two">
                <sui-statistic in-group>
                    <sui-statistic-value>{{ event.n_attendees }}</sui-statistic-value>
                    <sui-statistic-label>Participantes inscritos</sui-statistic-label>
                </sui-statistic>
                <sui-statistic in-group>
                    <sui-statistic-value>{{ event.n_attended }}</sui-statistic-value>
                    <sui-statistic-label>Participantes atenderam</sui-statistic-label>
                </sui-statistic>
            </sui-statistics-group>
        </div>
        <br>
        <div class="ui form">
            <div class="fields">
                <div class="twelve wide field">
                    <div class="ui left icon fluid input">
                        <i class="search icon"></i>
                        <input type="text" class="searchText" placeholder="Pesquisar..." v-model="searchText">
                    </div>
                </div>
                <div class="four wide field">
                    <DownloadButton v-bind:url="schedule.exports.feedback + event.id + '/'" />
                </div>
            </div>
        </div>
        <table class="ui striped sortable table tablet stackable structured">
            <thead>
                <tr>
                    <th class="sorted descending">Avaliação</th>
                    <th>Comentário</th>
                </tr>
            </thead>
            <tbody>
                <tr v-bind:key="feedback.id" v-for="feedback in filteredFeedbacks">
                    <td v-bind:data-sort-value="feedback.rating">
                        <div class="ui heart rating view" v-bind:data-rating="feedback.rating" data-max-rating=5></div>
                    </td>
                    <td>
                        {{ feedback.comments }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import DownloadButton from "project/components/extra/download_button.vue";

    export default {
        props: ["schedule_context", "event"],
        components: { DownloadButton },
        data() {
            return {
                schedule: this.schedule_context,
                searchText: '',
            };
        },
        computed: {
            filteredFeedbacks() {
                return this.event.feedbacks.filter(feedback => {
                    return (
                        feedback.comments
                        .toLowerCase()
                        .indexOf(this.searchText.toLowerCase()) > -1
                        );
                });
            },
            feedbackRatings() {
                return this.event.feedbacks.map(feedback => {
                    return feedback.rating;
                }).filter(feedback => {
                    return feedback && feedback > 0;
                })
            },
            rateColor() {
                return this.laplaceSmooth(this.feedbackRatings) < 2.5 ? 'red' : 'green';
            },
            rateText() {
                return this.feedbackRatings.length ? this.laplaceSmooth(this.feedbackRatings) : 'N/A';
            }
        },
        methods: {
            laplaceSmooth(list) {

                let alpha = 6,
                    beta = 2,
                    sum = list.reduce((a, b) => a + b, 0);
                return ((sum + alpha) / (list.length + beta)).toFixed(1);
            }
        },
        mounted() {
            $(".rating.view").rating();
            $(".rating.view").rating("disable");
            $(".table").tablesort();
            $('.question').popup()
        }
    };
</script>

<style scoped>
.dropdown,
.ui.form .fields .field .ui.input input,
.ui.form .field .ui.input input {
    margin-top: 10px;
}
.ui.button {
    border-radius: 0.28571429rem;
}
.actionbuttons {
    margin-top: 5px;
    margin-bottom: 5px;
}
.ui.icon.input > i.icon:not(.link) {
    margin-top: 7px;
}
.ui.table {
    font-size: 0.9em;
}
</style>
