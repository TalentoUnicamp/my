<template>
    <div>
        <br>
        <div>
            <h2 class="ui header centered">
                <div class="content">
                    Dados brutos
                    <div class="sub header">Aqui você pode visualizar e fazer o download dos dados brutos dos participantes<br>
                    Obs: Os dados da tabela estão reduzidos</div>
                </div>
            </h2>
        </div>
        <br>
        <div class="ui form">
            <div class="fields">
                <div class="twelve wide field">
                    <div class="ui left icon fluid input">
                        <i class="search icon"></i>
                        <input type="text" class="searchText" placeholder="Pesquisar por nome ou email" v-model="searchText">
                    </div>
                </div>
                <div class="four wide field">
                    <DownloadButton v-bind:url="stats.exports.all_hackers" />
                </div>
            </div>
        </div>
        <table class="ui striped table tablet stackable">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Email</th>
                </tr>
            </thead>
            <tbody>
                <tr v-bind:key="hacker.id" v-for="hacker in paginatedObjects">
                    <td>
                        <strong>
                            {{ hacker.profile.full_name }}
                        </strong>
                    </td>
                    <td>
                        {{ hacker.profile.email }}
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
import axios from "project/js/axios_csrf";
import swal from "sweetalert";
import toast from "project/js/notifications";

import DownloadButton from "project/components/extra/download_button.vue";

export default {
    props: ["stats_context"],
    components: { DownloadButton },
    data() {
        return {
            stats: this.stats_context,
            hackerList: [],
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
        filteredHackers() {
            return this.hackerList.filter(hacker => {
                let neename =
                    hacker.profile.full_name
                        .toLowerCase()
                        .indexOf(this.searchText.toLowerCase()) > -1;
                let neeemail =
                    hacker.profile.email
                        .toLowerCase()
                        .indexOf(this.searchText.toLowerCase()) > -1;
                return neename || neeemail;
            });
        },
        // Pagination stuff
        paginatedObjects() {
            let users = this.filteredHackers,
                lower = (this.selectedPage - 1) * this.pageSize,
                higher = Math.min(
                    this.selectedPage * this.pageSize - 1,
                    users.length
                );
            return users.slice(lower, higher);
        },
        maxPage() {
            return Math.max(
                Math.ceil(this.filteredHackers.length / this.pageSize),
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
        getHackerList() {
            var comp = this;
            axios
                .get(this.stats.exports.all_hackers + '?format=json')
                .then(function(data) {
                    comp.hackerList = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        }

    },
    mounted() {
        this.getHackerList();
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
</style>
