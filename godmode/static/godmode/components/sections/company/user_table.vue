<template>
    <div class="container">
        <br>
        <h2 class="ui header">
            <div class="content">
                Adicionar pessoas a empresas
                <div class="sub header">Selecione as pessoas e a empresa a qual deseja adicioná-las</div>
            </div>
        </h2>
        <sui-dropdown
        placeholder="Empresa"
        selection
        :options="companies"
        v-model="selectedCompany"
        />
        <sui-button v-bind:disabled="!canAdd" @click="$emit('add-to-company', selectedUsers, selectedCompany)" content="Adicionar" color="blue" />
        <div class="ui form">
            <div class="fields">
                <div class="sixteen wide field">
                    <div class="ui left icon fluid input">
                        <i class="search icon"></i>
                        <input type="text" class="searchText" placeholder="Pesquisar por nome ou email" v-model="searchUsers">
                    </div>
                </div>
            </div>
        </div>
        <table class="ui striped table tablet stackable">
            <thead>
                <tr>
                    <th><sui-checkbox v-model="selectAll" label="Selecionar todos" /></th>
                    <th>Nome</th>
                    <th>Email</th>
                </tr>
            </thead>
            <tbody class="user_list">
                <tr v-for="user in paginatedUsers" v-bind:key="user.unique_id">
                    <td>
                        <sui-checkbox v-bind:inputValue="selectedUsers.indexOf(user.unique_id) > -1" v-on:change="toggleUser(user.unique_id, $event)">
                        </sui-checkbox>
                    </td>
                    <td>
                        <strong>
                            {{ user.full_name }}
                        </strong>
                    </td>
                    <td>
                        {{ user.email }}
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
    props: ["userdata", "companydata"],
    data() {
        return {
            searchUsers: "",
            users: [],
            selectedUsers: [],
            companies: [],
            selectedCompany: null,
            selectAll: false,
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
        userdata: function(val) {
            this.users = val;
            this.selectedUsers = this.selectedUsers.filter(suser => {
                return (
                    this.users.findIndex(user => {
                        user.unique_id == suser;
                    }) > -1
                );
            });
        },
        companydata: function(val) {
            this.companies = val.map(company => {
                return {
                    key: company.id,
                    text: company.name,
                    value: company.id
                };
            });
        },
        selectAll: function(val) {
            this.toggleAll(val);
        },
        searchUsers: function(val) {
            this.selectedPage = 1;
        },
        pageSize: function(val) {
            this.selectedPage = 1;
        },
    },
    computed: {
        filteredUsers() {
            return this.users.filter(user => {
                let name =
                    user.full_name
                        .toLowerCase()
                        .indexOf(this.searchUsers.toLowerCase()) > -1;
                let email =
                    user.email
                        .toLowerCase()
                        .indexOf(this.searchUsers.toLowerCase()) > -1;
                return (name || email) && !user.is_employee;
            });
        },
        canAdd() {
            return (
                this.selectedCompany != null && this.selectedUsers.length > 0
            );
        },
        // Pagination stuff
        paginatedUsers() {
            let users = this.filteredUsers,
                lower = (this.selectedPage - 1) * this.pageSize,
                higher = Math.min(
                    this.selectedPage * this.pageSize - 1,
                    users.length
                );
            return users.slice(lower, higher);
        },
        maxPage() {
            return Math.max(Math.ceil(this.filteredUsers.length / this.pageSize), 1);
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
        toggleUser(unique_id, event) {
            if (!event) {
                let idx = this.selectedUsers.indexOf(unique_id);
                this.selectedUsers.splice(idx, 1);
            } else {
                this.selectedUsers.push(unique_id);
            }
        },
        toggleAll(event) {
            if (event) {
                this.selectedUsers = this.users.map(user => {
                    return user.unique_id;
                });
            } else {
                this.selectedUsers = [];
            }
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
