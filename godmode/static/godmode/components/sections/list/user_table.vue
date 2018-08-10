<template>
    <div class="container">
        <div class="ui form">
            <div class="fields">
                <div class="twelve wide field">
                    <div class="ui left icon fluid input">
                        <i class="search icon"></i>
                        <input type="text" class="searchText" placeholder="Pesquisar por nome" v-model="searchText">
                    </div>
                </div>
                <div class="four wide field">
                    <div id="hack_drop" class="ui floating fluid dropdown labeled icon button">
                        <i class="filter icon"></i>
                        <span class="text">Filtrar</span>
                        <div class="menu">
                            <div class="header">
                                <i class="tags icon"></i>
                                Filtrar por permissões
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
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Email</th>
                    <th>Estado</th>
                    <th>Atributos</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-bind:key="user.unique_id" v-for="user in paginatedUsers">
                    <td>
                        {{ user.unique_id }}
                    </td>
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
                    <td>
                        <sui-icon size="large" color="green" v-if="user.is_verified" name="check" />
                        <sui-icon size="large" color="blue" v-if="user.has_facebook" name="facebook" />
                        <sui-icon size="large" color="black" v-if="user.has_github" name="github" />
                        <sui-icon size="large" color="red" v-if="user.has_google" name="google" />
                    </td>

                    <td class="right aligned collapsing">
                        <sui-button class="actionbuttons" size="tiny" content="Hacker" v-bind:class="{blue: user.is_hacker, basic: !user.is_hacker }" @click="$emit('toggle-ishacker', user.unique_id)" />

                        <sui-button class="actionbuttons" size="tiny" content="Staff" v-bind:class="{blue: user.is_staff, basic: !user.is_staff }" @click="$emit('toggle-isstaff', user.unique_id)" />
                        <sui-button class="actionbuttons" size="tiny" content="Admin" v-bind:class="{blue: user.is_admin, basic: !user.is_admin }" @click="$emit('toggle-isadmin', user.unique_id)" />
                        <br>
                        <sui-button class="actionbuttons" size="tiny" content="Mentor" v-bind:class="{blue: user.is_mentor, basic: !user.is_mentor }" @click="$emit('toggle-ismentor', user.unique_id)" />
                        <sui-button class="actionbuttons" size="tiny" color="red" content="Apagar" @click="$emit('delete-user', user.unique_id)" />
                    </td>
                </tr>
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="3">
                        <div class="ui left floated">
                            <sui-dropdown
                            selection
                            :options="pageSizeOptions"
                            v-model="pageSize" />
                        </div>
                    </th>
                    <th colspan="3">
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
            filter: "",
            options: [
                { text: "Todos", color: "red" },
                { text: "Hacker", color: "blue" },
                { text: "Staff", color: "yellow" },
                { text: "Mentor", color: "orange" },
                { text: "Admin", color: "green" },
            ],
            users: this.data,
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
            let filtered = searched.filter(function(user) {
                if (self.filter === "Hacker") return user.is_hacker == true;
                if (self.filter === "Staff") return user.is_staff == true;
                if (self.filter === "Mentor") return user.is_mentor == true;
                if (self.filter === "Admin") return user.is_admin == true;
                return true;
            });
            return filtered;
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
                checkedin: "Checkin"
            };
            return map[state];
        }
    },
    mounted: function() {
        var comp = this;
        $("#hack_drop").dropdown({
            onChange: function(value) {
                comp.filter = value;
            }
        });
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
    font-size: 0.8em;
}
</style>
