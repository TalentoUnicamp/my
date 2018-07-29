<template>
    <div class="container">
        <div class="ui form">
            <div class="fields">
                <div class="eleven wide field">
                    <div class="ui left icon fluid input">
                        <i class="search icon"></i>
                        <input type="text" class="searchText" placeholder="Pesquisar por nome e email" v-model="searchText">
                    </div>
                </div>
                <div class="five wide field">
                    <div id="filter_drop" class="ui floating fluid dropdown labeled icon button">
                        <i class="filter icon"></i>
                        <span class="text">Filtrar</span>
                        <div class="menu">
                            <div class="header">
                                <i class="tags icon"></i>
                                Filtrar por estado
                            </div>
                            <div class="scrolling menu">
                                <div v-bind:key="option.text" v-for="option in options" v-bind:data-value="option.text" class="item">
                                    <div v-bind:class="option.color" class="ui empty circular label"></div>
                                    {{ option.text }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <table class="ui striped table tablet stackable">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Email</th>
                    <th>Estado</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-bind:key="user.email" v-for="user in paginatedUsers">
                    <td>
                        <strong>
                            {{ user.full_name }}
                        </strong>
                    </td>
                    <td>
                        {{ user.email }}
                    </td>
                    <td>
                        <strong>
                            {{ user.state | mapState }}
                        </strong>
                    </td>
                    <td class="right aligned collapsing">

                        <sui-button
                        class="actionbuttons"
                        size="tiny"
                        content="Analisar"
                        color="blue"
                        v-if="user.state == 'submitted'"
                        @click="analyzeHacker(user.unique_id)" />

                        <sui-button
                        class="actionbuttons"
                        size="tiny"
                        content="Rejeitar"
                        color="red"
                        v-if="user.state == 'admitted' || user.state == 'confirmed'"
                        @click="rejectHacker(user.unique_id)" />

                        <sui-button
                        class="actionbuttons"
                        size="tiny"
                        content="Admitir"
                        color="green"
                        v-if="user.state == 'declined'"
                        @click="admitHacker(user.unique_id)" />

                        <sui-button
                        class="actionbuttons"
                        size="tiny"
                        content="Tirar da fila"
                        color="orange"
                        v-if="user.state == 'waitlist'"
                        @click="unWaitlistHacker(user.unique_id)" />

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
        <sui-modal v-model="openAnalyzeModal">

            <sui-dimmer v-bind:active="applicationData === null" inverted>
                <sui-loader content="Carregando hacker..." />
            </sui-dimmer>
                <sui-modal-header v-if="applicationData !== null">{{ applicationData.full_name }}</sui-modal-header>
                <sui-modal-content v-if="applicationData !== null">
                    <sui-modal-description>
                        <sui-header>Default Profile Image</sui-header>
                        <p>We've found the following gravatar image associated with your e-mail address.</p>
                        <p>Is it okay to use this photo?</p>
                    </sui-modal-description>
                </sui-modal-content>
                <sui-modal-actions v-if="applicationData !== null">
                    <div @click="rejectHacker(applicationData.unique_id)" class="ui negative right labeled icon button">Rejeitar<sui-icon name="times" /></div>
                    <div @click="admitHacker(applicationData.unique_id)" class="ui positive right labeled icon button">Admitir<sui-icon name="check" /></div>
                </sui-modal-actions>
        </sui-modal>
    </div>

</template>

<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import swal from "sweetalert";

export default {
    props: ["data", "staff_context"],
    data() {
        return {
            staff: this.staff_context,
            searchText: "",
            filter: "",
            options: [
                { text: "Todos", color: "orange" },
                { text: "Submetido", color: "black" },
                { text: "Admitido", color: "yellow" },
                { text: "Confirmado", color: "blue" },
                { text: "Fila de espera", color: "gray" },
                { text: "Check-in", color: "green" },
                { text: "Recusado", color: "red" }
            ],
            users: [],
            openAnalyzeModal: false,
            applicationData: null,
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
            this.users = val;
        },
        searchText: function(val) {
            this.selectedPage = 1;
        },
        pageSize: function(val) {
            this.selectedPage = 1;
        },
        filter: function(val) {
            this.selectedPage = 1;
        }
    },
    computed: {
        filteredUsers() {
            let searched = this.users.filter(user => {
                let byname =
                    user.full_name
                        .toLowerCase()
                        .indexOf(this.searchText.toLowerCase()) > -1;
                let byemail =
                    user.email
                        .toLowerCase()
                        .indexOf(this.searchText.toLowerCase()) > -1;
                return byname || byemail;
            });
            if (this.filter === "") return searched;
            self = this;
            return searched.filter(function(user) {
                if (self.filter == "" || self.filter == "Todos") return true;
                return (
                    self.$options.filters.mapState(user.state) == self.filter
                );
            });
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
            return Math.max(
                Math.ceil(this.filteredUsers.length / this.pageSize),
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
    filters: {
        mapState: function(state) {
            var map = {
                unverified: "Não verificado",
                verified: "Verificado",
                incomplete: "Incompleto",
                submitted: "Submetido",
                late: "Atrasado",
                declined: "Recusado",
                admitted: "Admitido",
                waitlist: "Fila de espera",
                withdraw: "Desistente",
                confirmed: "Confirmado",
                checkedin: "Check-in"
            };
            return map[state];
        }
    },
    mounted: function() {
        var comp = this;
        $("#filter_drop").dropdown({
            onChange: function(value) {
                comp.filter = value;
            }
        });
    },
    methods: {
        analyzeHacker(unique_id) {
            this.applicationData = null;
            this.openAnalyzeModal = true;
            self = this;
            axios
                .get(this.staff.api.view_application + unique_id)
                .then(function(data) {
                    self.applicationData = data.data;
                    console.log(data.data);
                })
                .catch(function(error) {
                    console.error(error);
                    self.openAnalyzeModal = false;
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        rejectHacker(unique_id) {
            this.openAnalyzeModal = false;
            let useridx = this.users.findIndex(u => u.unique_id == unique_id);
            let user = this.users[useridx];
            var comp = this;
            swal({
                title: "Rejeitar " + user.full_name,
                text: "Tem certeza de que quer fazer isso?",
                icon: "warning",
                dangerMode: true,
                buttons: ["Calma aí", "Rejeitar!"]
            }).then(isRejecting => {
                if (isRejecting) {
                    axios
                        .post(comp.staff.api.decline_hacker, {
                            unique_id: unique_id
                        })
                        .then(function(data) {
                            toast("Atenção", data.data.message, "info");
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
        admitHacker(unique_id) {
            this.openAnalyzeModal = false;
            let useridx = this.users.findIndex(u => u.unique_id == unique_id);
            let user = this.users[useridx];
            var comp = this;
            swal({
                title: "Admitir " + user.full_name,
                text: "Tem certeza de que quer fazer isso?",
                icon: "warning",
                buttons: ["Calma aí", "Admitir!"]
            }).then(isAdmitting => {
                if (isAdmitting) {
                    axios
                        .post(comp.staff.api.admit_hacker, {
                            unique_id: unique_id
                        })
                        .then(function(data) {
                            toast("Sucesso", data.data.message, "success");
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
        unWaitlistHacker(unique_id) {
            let useridx = this.users.findIndex(u => u.unique_id == unique_id);
            let user = this.users[useridx];
            var comp = this;
            swal({
                title: "Tirar da fila de espera ",
                text:
                    "Tem certeza de que quer tirar " +
                    user.full_name +
                    " da fila de espera?",
                icon: "warning",
                buttons: ["Calma aí", "Sim!"]
            }).then(isUnwaitlist => {
                if (isUnwaitlist) {
                    axios
                        .post(comp.staff.api.unwaitlist_hacker, {
                            unique_id: unique_id
                        })
                        .then(function(data) {
                            toast("Sucesso", data.data.message, "success");
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
.ui.icon.input > i.icon:not(.link) {
    margin-top: 7px;
}
</style>
