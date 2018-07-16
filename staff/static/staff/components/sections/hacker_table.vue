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
                    <div id="filter_drop" class="ui floating fluid dropdown labeled icon button">
                        <i class="filter icon"></i>
                        <span class="text">Filtrar</span>
                        <div class="menu">
                            <div class="header">
                                <i class="tags icon"></i>
                                Filtrar por estado
                            </div>
                            <div class="scrolling menu">
                                <div v-for="option in options" v-bind:data-value="option.text" class="item">
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
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in filteredUsers">
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
                </tr>
            </tbody>
        </table>

    </div>

</template>

<script>

    export default {
        props: ['data'],
        data() {
            return {
                searchText: '',
                filter: '',
                options: [
                {text: 'Todos', color: 'red'},
                {text: 'Confirmado', color: 'blue'},
                {text: 'Admitido', color: 'yellow'},
                {text: 'Fila de espera', color: 'gray'},
                {text: 'Checkin', color: 'green'},
                ],
                users: []
            }
        },
        watch: {
            data: function(val) {
                this.users = val;
            }
        },
        computed: {
            filteredUsers() {
                let searched = this.users.filter(user => {
                    let byname = user.full_name.toLowerCase().indexOf(this.searchText.toLowerCase()) > -1
                    let byemail = user.email.toLowerCase().indexOf(this.searchText.toLowerCase()) > -1
                    return byname || byemail;
                });
                if (this.filter === '')
                    return searched;
                self = this;
                return searched.filter(function (user) {
                    if (self.filter == '' || self.filter == 'Todos')
                        return true;
                    return self.$options.filters.mapState(user.state) == self.filter;
                });
            }
        },
        filters: {
            mapState: function(state) {
                var map = {
                    unverified: 'Não verificado',
                    verified: 'Verificado',
                    incomplete: 'Incompleto',
                    submitted: 'Submetido',
                    late: 'Atrasado',
                    declined: 'Recusado',
                    admitted: 'Admitido',
                    waitlist: 'Fila de espera',
                    withdraw: 'Desistente',
                    confirmed: 'Confirmado',
                    checkedin: 'Checkin'
                };
                return map[state];
            }
        },
        mounted: function () {
            var comp = this;
            $("#filter_drop").dropdown({
                onChange: function (value) {
                    comp.filter = value;
                }
            })
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
.ui.icon.input > i.icon:not(.link) {
    margin-top: 7px;
}
.ui.table {
    font-size: .8em;
}
</style>
