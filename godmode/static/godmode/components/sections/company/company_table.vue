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
                <tr v-for="company in filteredCompanies" v-bind:key="company.id">
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
                newCompanyAccess: null
            };
        },
        watch: {
            data: function(val) {
                this.companies = val;
            }
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
            }
        },
        methods: {
            createCompany() {
                this.$emit("create-company", {name: this.newCompanyName, access_level: this.newCompanyAccess});
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
