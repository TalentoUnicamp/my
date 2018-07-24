<template>
    <div class="container">
        <br>
        <div>
            <h2 class="ui header divided centered">
                <div class="content">
                    Anúncios
                    <div class="sub header">Aqui você pode criar anúncios que serão vistos por todos os usuários em telas específicas</div>
                </div>
            </h2>
        </div>
        <sui-divider />
        <sui-form @submit.prevent="createAnnouncement">
            <sui-form-field>
                <label>Título do anúncio</label>
                <sui-input v-model="title" type='text' placeholder="Meu anúncio" />
            </sui-form-field>
            <sui-form-field>
                <label>Texto do anúncio</label>
                <textarea v-model="text"></textarea>
            </sui-form-field>
            <sui-form-field>
                <label>Tipo de anúncio</label>
                <sui-dropdown
                fluid
                :options="levelOptions"
                placeholder="Selecione um tipo"
                selection
                v-model="level" />
            </sui-form-field>
            <sui-button fluid content="Criar anúncio" color="blue"
            v-bind:loading="createLoading"
            v-bind:disabled="createLoading || title.length == 0 || text.length == 0 || level.length == 0" />
        </sui-form>
        <br>
        <sui-divider />
        <br>
        <Announcement
        v-for="announcement in announcementList"
        v-bind:key="announcement.id"
        v-bind:announcement="announcement"
        v-bind:allowDelete="true"
        @delete-announcement="deleteAnnouncement" />
    </div>
</template>

<script>
    import axios from "project/js/axios_csrf"
    import toast from "project/js/notifications"
    import Announcement from "announcement/components/announcement.vue"

    import { ModelSubscription } from 'model_sockets/js/subscription';

    export default {
        components: { Announcement },
        props: ['admin_context'],
        data() {
            return {
                admin: admin_context,
                announcementList: [],
                levelOptions: [],
                createLoading: false,
                title: '',
                text: '',
                level: ''
            }
        },
        methods: {
            getAnnouncementList() {
                var comp = this;
                axios.get(this.admin.api.list_announcement)
                .then(function (data) {
                    comp.announcementList = data.data;
                })
                .catch(function (error) {
                    console.error(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            },
            getLevelOptions() {
                var comp = this;
                axios.options(this.admin.api.create_announcement)
                .then(function (data) {
                    comp.levelOptions = data.data.actions.POST.level.choices.map(choice => {
                        return {
                            key: choice.value,
                            value: choice.value,
                            text: choice.display_name
                        }
                    });
                })
                .catch(function (error) {
                    console.error(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            },
            announcementCreated(announcement) {
                this.announcementList.unshift(announcement);
            },
            announcementDeleted(announcement) {
                let annIdx = this.announcementList.findIndex((obj => obj.id == announcement.id));
                this.announcementList.splice(annIdx, 1);
            },
            createAnnouncement() {
                self = this;
                this.createLoading = true;
                axios.post(this.admin.api.create_announcement, {
                    title: this.title,
                    text: this.text,
                    level: this.level
                })
                .then(function(data) {
                    self.title = '';
                    self.text = '';
                    self.level = '';
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                })
                .then(function() {
                    self.createLoading = false;
                });
            },
            deleteAnnouncement(id) {
                self = this;
                axios.delete(this.admin.api.delete_announcement + id)
                .then(function(data) {
                    toast('Aviso', 'Anúncio removido', 'info');
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
            }
        },
        mounted: function () {
            this.getAnnouncementList();
            this.getLevelOptions();

            var createsub = new ModelSubscription('announcement', 'Announcement', 'create');
            var deletesub = new ModelSubscription('announcement', 'Announcement', 'delete');
            createsub.connect();
            deletesub.connect();
            createsub.subscribe(this.announcementCreated);
            deletesub.subscribe(this.announcementDeleted);
        }
    }
</script>
