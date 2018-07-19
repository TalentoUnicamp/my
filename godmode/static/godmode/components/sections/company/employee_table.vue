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
                    <th>Empresa</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="employee in filteredEmployees" v-bind:key="employee.unique_id">
                    <td>
                        <strong>
                            {{ employee.full_name }}
                        </strong>
                    </td>
                    <td>
                        {{ employee.email }}
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
        </table>
    </div>
</template>

<script>
export default {
    props: ["data"],
    data() {
        return {
            searchEmployees: "",
            employees: []
        };
    },
    watch: {
        data: function(val) {
            this.employees = val;
        }
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
