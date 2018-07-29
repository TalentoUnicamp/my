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
        <table class="ui striped table tablet stackable structured">
            <thead>
                <tr>
                    <th>Avaliação</th>
                    <th>Comentário</th>
                </tr>
            </thead>
            <tbody>
                <tr v-bind:key="feedback.id" v-for="feedback in paginatedObjects">
                    <td>
                        <div class="ui heart rating view" v-bind:data-rating="feedback.rating" data-max-rating=5></div>
                    </td>
                    <td>
                        {{ feedback.comments }}
                    </td>
                </tr>
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="1">
                        <div class="ui left floated">
                            <sui-dropdown
                            selection
                            :options="pageSizeOptions"
                            v-model="pageSize" />
                        </div>
                    </th>
                    <th colspan="1">
                        <div class="ui right floated pagination menu">
                            <a class="item"
                            v-for="page in pages"
                            :class="{active: page === selectedPage}"
                            :key="page"
                            @click="selectedPage = page">
                                {{ page }}
                            </a>
                        </div>
                    </th>
                </tr>
            </tfoot>
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
            searchText: "",
            selectedPage: 1,
            pageSize: 20,
            pageSizeOptions: [
                { value: 10, text: "10" },
                { value: 20, text: "20" },
                { value: 50, text: "50" },
                { value: 100, text: "100" }
            ]
        };
    },
    watch: {
        searchText: function(val) {
            this.selectedPage = 1;
        },
        pageSize: function(val) {
            this.selectedPage = 1;
        }
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
            return this.event.feedbacks
                .map(feedback => {
                    return feedback.rating;
                })
                .filter(feedback => {
                    return feedback && feedback > 0;
                });
        },
        rateColor() {
            return this.laplaceSmooth(this.feedbackRatings) < 2.5
                ? "red"
                : "green";
        },
        rateText() {
            return this.feedbackRatings.length
                ? this.laplaceSmooth(this.feedbackRatings)
                : "N/A";
        },
        // Order scans by rating (desc)
        orderedObjects() {
            return this.filteredFeedbacks.slice(0).sort((obj1, obj2) => {
                return obj2.rating - obj1.rating;
            });
        },
        // Pagination stuff
        paginatedObjects() {
            let users = this.orderedObjects,
                lower = (this.selectedPage - 1) * this.pageSize,
                higher = Math.min(
                    this.selectedPage * this.pageSize - 1,
                    users.length
                );
            return users.slice(lower, higher);
        },
        maxPage() {
            return Math.max(
                Math.ceil(this.orderedObjects.length / this.pageSize),
                1
            );
        },
        pages() {
            if (this.maxPage < 7)
                return Array.from({ length: this.maxPage }, (x, i) => i + 1);
            if (this.selectedPage <= 4) return [1, 2, 3, 4, 5, 6, this.maxPage];
            if (this.selectedPage + 2 < this.maxPage)
                return [
                    1,
                    this.selectedPage - 2,
                    this.selectedPage - 1,
                    this.selectedPage,
                    this.selectedPage + 1,
                    this.selectedPage + 2,
                    this.maxPage
                ];
            return [
                1,
                this.maxPage - 5,
                this.maxPage - 4,
                this.maxPage - 3,
                this.maxPage - 2,
                this.maxPage - 1,
                this.maxPage
            ];
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
        $(".question").popup();
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
