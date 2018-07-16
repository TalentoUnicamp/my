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
                <tr v-for="user in filteredUsers">
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
        </table>
    </div>
</template>

<script>

    export default {
        props: ['userdata', 'companydata'],
        data() {
            return {
                searchUsers: '',
                users: [],
                selectedUsers: [],
                companies: [],
                selectedCompany: null,
                selectAll: false
            }
        },
        watch: {
            userdata: function(val) {
                this.users = val;
                this.selectedUsers = this.selectedUsers.filter(suser => {
                    return this.users.findIndex(user => {user.unique_id == suser}) > -1
                })

            },
            companydata: function(val) {
                this.companies = val.map(company => {
                    return {
                        key: company.id,
                        text: company.name,
                        value: company.id
                    }
                })
            },
            selectAll: function(val) {
                this.toggleAll(val);
            }
        },
        computed: {
            filteredUsers() {
                return this.users.filter(user => {
                    let name = user.full_name.toLowerCase().indexOf(this.searchUsers.toLowerCase()) > -1
                    let email = user.email.toLowerCase().indexOf(this.searchUsers.toLowerCase()) > -1
                    return (name || email) && !user.is_employee;
                });
            },
            canAdd() {
                return this.selectedCompany != null && this.selectedUsers.length > 0;
            }
        },
        methods: {
            toggleUser(unique_id, event) {
                if (!event) {
                    let idx = this.selectedUsers.indexOf(unique_id);
                    this.selectedUsers.splice(idx, 1);
                }
                else {
                    this.selectedUsers.push(unique_id);
                }
            },
            toggleAll(event) {
                if (event) {
                    this.selectedUsers = this.users.map(user => {
                        return user.unique_id;
                    })
                }
                else {
                    this.selectedUsers = [];
                }
            }
        }
    }
</script>

<style scoped>
.dropdown, .ui.form .fields .field .ui.input input, .ui.form .field .ui.input input {
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
    font-size: .8em;
}
</style>
