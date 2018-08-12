<template>
    <div>
        <div class="ui stackable centered">
            <div class="column">
                <sui-menu class="stackable four item">
                    <a
                    is="sui-menu-item"
                    v-for="item in items"
                    :active="isActive(item)"
                    :key="item"
                    :content="item"
                    @click="select(item)"
                    />
                </sui-menu>

                <UserList
                v-bind:userdata="userList"
                v-bind:companydata="companyList"
                v-on:add-to-company="createEmployee"
                v-show="isActive('Não empregados')" />
                <EmployeeList
                v-bind:data="employeeList"
                v-on:remove-from-company="deleteEmployee"
                v-show="isActive('Empregados')" />
                <Checkin
                v-bind:admin_context="admin"
                v-show="isActive('Check in')" />
                <CompanyList
                v-bind:data="companyList"
                v-on:create-company="createCompany"
                v-on:delete-company="deleteCompany"
                v-show="isActive('Empresas')" />

            </div>
        </div>
    </div>
</template>

<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import swal from "sweetalert";

import CompanyList from "./company/company_table.vue";
import EmployeeList from "./company/employee_table.vue";
import UserList from "./company/user_table.vue";
import Checkin from "./company/checkin.vue";

import { ModelSubscription } from "model_sockets/js/subscription";

export default {
    props: ["admin_context"],
    components: { CompanyList, EmployeeList, UserList, Checkin },
    data() {
        return {
            admin: this.admin_context,
            companyList: [],
            employeeList: [],
            userList: [],
            active: "Não empregados",
            items: ["Não empregados", "Empregados", "Check in", "Empresas"]
        };
    },
    methods: {
        isActive(name) {
            return this.active === name;
        },
        select(name) {
            this.active = name;
        },

        // Company methods
        getCompanyList() {
            self = this;
            axios
                .get(this.admin.api.list_companies)
                .then(function(data) {
                    self.companyList = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        companyCreated(company) {
            this.companyList = addToList(this.companyList, company);
        },
        companyDeleted(company) {
            this.companyList = deleteFromList(this.companyList, company, "id");
        },
        deleteCompany(company_id) {
            swal({
                title: "Tem certeza?",
                text: "Essa ação é irreversível!",
                icon: "warning",
                buttons: ["Cancelar", "Apagar"],
                dangerMode: true
            }).then(willDelete => {
                if (willDelete) {
                    axios
                        .delete(this.admin.api.delete_company + company_id)
                        .then(function(data) {
                            toast("Aviso", "Empresa apagada", "info");
                        })
                        .catch(function(error) {
                            console.error(error);
                            toast(
                                "Opa!",
                                "Algo de errado aconteceu :(",
                                "error"
                            );
                        });
                }
            });
        },
        createCompany(company_data) {
            axios
                .post(this.admin.api.create_company, company_data)
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },

        // Employee methods
        getEmployeeList() {
            self = this;
            axios
                .get(this.admin.api.list_employees)
                .then(function(data) {
                    self.employeeList = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        employeeCreated(employee) {
            this.employeeList = addToList(this.employeeList, employee);
        },
        employeeUpdated(employee) {
            this.employeeList = updateOnList(
                this.employeeList,
                employee,
                "unique_id"
            );
        },
        employeeDeleted(employee) {
            this.employeeList = deleteFromList(
                this.employeeList,
                employee,
                "unique_id"
            );
        },
        deleteEmployee(unique_id) {
            axios
                .delete(this.admin.api.delete_employee + unique_id)
                .then(function(data) {
                    toast("Aviso", "Empregado removido", "info");
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },

        // Non employee methods
        getUserList() {
            self = this;
            axios
                .get(this.admin.api.list_profiles)
                .then(function(data) {
                    self.userList = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        userCreated(user) {
            this.userList = addToList(this.userList, user);
        },
        userUpdated(user) {
            this.userList = updateOnList(this.userList, user, "unique_id");
        },
        userDeleted(user) {
            this.userList = deleteFromList(this.userList, user, "unique_id");
        },
        createEmployee(employeeList, companyId) {
            for (var employee in employeeList) {
                let unique_id = employeeList[employee];
                axios
                    .post(this.admin.api.create_employee, {
                        unique_id: unique_id,
                        company_id: companyId
                    })
                    .catch(function(error) {
                        console.error(error);
                        toast("Opa!", "Algo de errado aconteceu :(", "error");
                    });
            }
        }
    },
    mounted: function() {
        // Companies
        this.getCompanyList();
        var createcompany = new ModelSubscription(
            "company",
            "Company",
            "create"
        );
        var deletecompany = new ModelSubscription(
            "company",
            "Company",
            "delete"
        );
        createcompany.connect();
        deletecompany.connect();
        createcompany.subscribe(this.companyCreated);
        deletecompany.subscribe(this.companyDeleted);

        // Employees
        this.getEmployeeList();
        var createemployee = new ModelSubscription(
            "company",
            "Employee",
            "create"
        );
        var updateemployee = new ModelSubscription(
            "company",
            "Employee",
            "update"
        );
        var deleteemployee = new ModelSubscription(
            "company",
            "Employee",
            "delete"
        );
        createemployee.connect();
        updateemployee.connect();
        deleteemployee.connect();
        createemployee.subscribe(this.employeeCreated);
        updateemployee.subscribe(this.employeeUpdated);
        deleteemployee.subscribe(this.employeeDeleted);

        // Users
        this.getUserList();
        var createuser = new ModelSubscription(
            "user_profile",
            "Profile",
            "create"
        );
        var updateuser = new ModelSubscription(
            "user_profile",
            "Profile",
            "update"
        );
        var deleteuser = new ModelSubscription(
            "user_profile",
            "Profile",
            "delete"
        );
        createuser.connect();
        updateuser.connect();
        deleteuser.connect();
        createuser.subscribe(this.userCreated);
        updateuser.subscribe(this.userUpdated);
        deleteuser.subscribe(this.userDeleted);
    }
};

function deleteFromList(list, user, id_field) {
    return list.filter(obj => {
        return user[id_field] != obj[id_field];
    });
}
function updateOnList(list, user, id_field) {
    return list.map(obj => {
        if (user[id_field] != obj[id_field]) return obj;
        return user;
    });
}
function addToList(list, user) {
    list.push(user);
    return list;
}
</script>
