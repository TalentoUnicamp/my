<template>
    <div class="container">
        <div class="ui form">
            <div class="fields">
                <div class="sixteen wide field">
                    <div class="ui left icon fluid input">
                        <i class="search icon"></i>
                        <input type="text" class="searchText" placeholder="Pesquisar por nome, email ou empresa" v-model="searchEmployees" />
                    </div>
                </div>
            </div>
        </div>
        <table class="ui striped table tablet stackable">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Email</th>
                    <th>Check in</th>
                    <th>Empresa</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="employee in paginatedUsers" v-bind:key="employee.unique_id">
                    <td>
                        <strong>
                            {{ employee.full_name }}
                        </strong>
                    </td>
                    <td>
                        {{ employee.email }}
                    </td>
                    <td>
                        <sui-icon size="large" :color="employee.checkedin ? 'green' : 'red'" :name="employee.checkedin ? 'check' : 'times'" />
                    </td>
                    <td>
                        <strong>
                            {{ employee.company_name }}
                        </strong>
                    </td>
                    <td class="right aligned collapsing">
                        <sui-button class="actionbuttons" content="Remover" color="red" @click="$emit('remove-from-company', employee.unique_id)" />
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
                    <th colspan="4">
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
            searchEmployees: "",
            employees: [],
            selectedPage: 1,
            pageSize: 20,
            pageSizeOptions: [
                { value: 10, text: "10" },
                { value: 20, text: "20" },
                { value: 50, text: "50" },
                { value: 100, text: "100" }
            ],
        };
    },
    watch: {
        data: function(val) {
            this.employees = val;
        },
        searchEmployees: function(val) {
            this.selectedPage = 1;
        },
        pageSize: function(val) {
            this.selectedPage = 1;
        },
    },
    computed: {
        filteredEmployees() {
            return this.employees.filter(employee => {
                let name =
                    employee.full_name
                        .toLowerCase()
                        .indexOf(this.searchEmployees.toLowerCase()) > -1;
                let email =
                    employee.email
                        .toLowerCase()
                        .indexOf(this.searchEmployees.toLowerCase()) > -1;
                let company =
                    employee.company_name
                        .toLowerCase()
                        .indexOf(this.searchEmployees.toLowerCase()) > -1;
                return name || email || company;
            });
        },
        // Pagination stuff
        paginatedUsers() {
            let users = this.filteredEmployees,
                lower = (this.selectedPage - 1) * this.pageSize,
                higher = Math.min(
                    this.selectedPage * this.pageSize - 1,
                    users.length
                );
            return users.slice(lower, higher);
        },
        maxPage() {
            return Math.max(Math.ceil(this.filteredEmployees.length / this.pageSize), 1);
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
