<template>
    <div>
        <br>
        <div class="small title">
            Lista de usuários
        </div>
        <UserTable
        v-bind:data="userList"
        v-on:toggle-ishacker="toggleIsHacker"
        v-on:toggle-isstaff="toggleIsStaff"
        v-on:toggle-isadmin="toggleIsAdmin"
        v-on:toggle-ismentor="toggleIsMentor"
        v-on:delete-user="deleteUser" />
    </div>
</template>

<script>
    import axios from 'project/js/axios_csrf';
    import toast from 'project/js/notifications';
    import swal from 'sweetalert';
    import UserTable from './list/user_table.vue';

    import { ModelSubscription } from 'model_sockets/js/subscription';

    export default {
        components: { UserTable },
        props: ['admin_context'],
        data() {
            return {
                admin: this.admin_context,
                userList: []
            }
        },
        methods: {
            getUserList() {
                var comp = this;
                axios.get(this.admin.api.list_profiles)
                .then(function (data) {
                    comp.userList = data.data;
                })
                .catch(function (error) {
                    console.error(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            },
            userUpdated(user) {
                let userIdx = this.userList.findIndex((obj => obj.unique_id == user.unique_id));
                this.userList.splice(userIdx, 1, user);
            },
            userCreated(user) {
                this.userList.push(user);
            },
            userDeleted(user) {
                let userIdx = this.userList.findIndex((obj => obj.unique_id == user.unique_id));
                this.userList.splice(userIdx, 1);
            },
            toggleIsHacker(unique_id) {
                let idx = this.userList.findIndex((obj => obj.unique_id == unique_id));
                if (this.userList[idx].is_hacker && this.userList[idx].state != 'incomplete') {
                    swal({
                        title: 'Tem certeza?',
                        text: 'Esse usuário perderá seu formulário de aplicação e qualquer outra propriedade associada ao seu status de hacker!',
                        icon: 'warning',
                        buttons: ["Cancelar", "Alterar"],
                        dangerMode: true,
                    })
                    .then((willDelete) => {
                        if (willDelete) {
                            axios.post(this.admin.api.toggle_is_hacker, {
                                unique_id: unique_id
                            })
                            .then(function(data) {
                                toast('Aviso', data.data.message, 'info');
                            })
                            .catch(function (error) {
                                console.error(error);
                                toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                            });
                        }
                    })
                }
                else {
                    axios.post(this.admin.api.toggle_is_hacker, {
                        unique_id: unique_id
                    })
                    .then(function(data) {
                        toast('Aviso', data.data.message, 'info');
                    })
                    .catch(function (error) {
                        console.error(error);
                        toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                    });
                }
            },
            toggleIsStaff(unique_id) {
                var comp = this;
                axios.post(this.admin.api.toggle_is_staff, {
                    unique_id: unique_id
                })
                .then(function(data) {
                    toast('Aviso', data.data.message, 'info');
                })
                .catch(function (error) {
                    console.error(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            },
            toggleIsMentor(unique_id) {
                var comp = this;
                axios.post(this.admin.api.toggle_is_mentor, {
                    unique_id: unique_id
                })
                .then(function(data) {
                    toast('Aviso', data.data.message, 'info');
                })
                .catch(function (error) {
                    console.error(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            },
            toggleIsAdmin(unique_id) {
                var comp = this;
                axios.post(this.admin.api.toggle_is_admin, {
                    unique_id: unique_id
                })
                .then(function(data) {
                    toast('Aviso', data.data.message, 'info');
                })
                .catch(function (error) {
                    console.error(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            },
            deleteUser(unique_id) {
                swal({
                    title: 'Tem certeza?',
                    text: 'Essa ação é irreversível!',
                    icon: 'warning',
                    buttons: ["Cancelar", "Apagar"],
                    dangerMode: true,
                })
                .then((willDelete) => {
                    if (willDelete) {
                        axios.delete(this.admin.api.delete_user + unique_id)
                        .then(function(data) {
                            toast('Aviso', 'Usuário removido', 'info');
                        })
                        .catch(function (error) {
                            console.error(error);
                            toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                        });
                    }
                })
            }
        },
        mounted: function () {
            this.getUserList();

            var updatesub = new ModelSubscription('user_profile', 'Profile', 'update');
            var createsub = new ModelSubscription('user_profile', 'Profile', 'create');
            var deletesub = new ModelSubscription('user_profile', 'Profile', 'delete');
            updatesub.connect();
            createsub.connect();
            deletesub.connect();
            updatesub.subscribe(this.userUpdated);
            createsub.subscribe(this.userCreated);
            deletesub.subscribe(this.userDeleted);
        }
    }
</script>
