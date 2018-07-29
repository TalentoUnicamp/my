<template>
    <div class="container">
        <sui-form v-on:submit.prevent="createCompany">
            <sui-form-fields fields='two'>
                <sui-form-field>
                    <label>Nome da empresa</label>
                    <input placeholder="Nome" v-model="newCompanyName">
                </sui-form-field>
                <sui-form-field>
                    <label>Nível de acesso</label>
                    <input type="number" min="0" max="10" placeholder="Inteiros positivos" v-model="newCompanyAccess">
                </sui-form-field>
            </sui-form-fields>
            <sui-button content="Criar empresa" color="blue" />
        </sui-form>
        <sui-divider />
        <div class="ui form">
            <div class="fields">
                <div class="sixteen wide field">
                    <div class="ui left icon fluid input">
                        <i class="search icon"></i>
                        <input type="text" class="searchText" placeholder="Pesquisar por nome" v-model="searchText">
                    </div>
                </div>
            </div>
        </div>
        <table class="ui striped table tablet stackable">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Acesso</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="company in paginatedObjects" v-bind:key="company.id">
                    <td>
                        {{ company.id }}
                    </td>
                    <td>
                        <strong>
                            {{ company.name }}
                        </strong>
                    </td>
                    <td>
                        {{ company.access_level }}
                    </td>
                    <td class="right aligned collapsing">
                        <sui-button class="actionbuttons" content="Apagar" color="red" @click="$emit('delete-company', company.id)" />
                    </td>
                </tr>
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="2">
                        <div class="ui left floated">
                            <sui-dropdown
                            selection
                            :options="pageSizeOptions"
                            v-model="pageSize" />
                        </div>
                    </th>
                    <th colspan="2">
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
export default {
    props: ["data"],
    data() {
        return {
            searchText: "",
            companies: this.data,
            newCompanyName: "",
            newCompanyAccess: null,
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
        data: function(val) {
            this.companies = val;
        },
        searchText: function(val) {
            this.selectedPage = 1;
        },
        pageSize: function(val) {
            this.selectedPage = 1;
        },
    },
    computed: {
        filteredCompanies() {
            return this.companies.filter(company => {
                return (
                    company.name
                        .toLowerCase()
                        .indexOf(this.searchText.toLowerCase()) > -1
                );
            });
        },
        // Pagination stuff
        paginatedObjects() {
            let users = this.filteredCompanies,
                lower = (this.selectedPage - 1) * this.pageSize,
                higher = Math.min(
                    this.selectedPage * this.pageSize - 1,
                    users.length
                );
            return users.slice(lower, higher);
        },
        maxPage() {
            return Math.max(Math.ceil(this.filteredCompanies.length / this.pageSize), 1);
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
        createCompany() {
            this.$emit("create-company", {
                name: this.newCompanyName,
                access_level: this.newCompanyAccess
            });
            this.newCompanyName = "";
            this.newCompanyAccess = null;
            return null;
        }
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
