<template>
    <div>
        <br>
        <div>
            <h2 class="ui header centered">
                <div class="content">
                    Lista de eventos
                </div>
            </h2>
        </div>
        <br>
        <div class="ui form">
            <div class="fields">
                <div class="twelve wide field">
                    <div class="ui left icon fluid input">
                        <i class="search icon"></i>
                        <input type="text" class="searchText" placeholder="Pesquisar..." v-model="searchText">
                    </div>
                </div>
                <div class="four wide field">
                    <DownloadButton v-bind:url="schedule.exports.event_list" />
                </div>
            </div>
        </div>
        <table class="ui striped table tablet stackable">
            <thead>
                <tr>
                    <th>Evento</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-bind:key="event.id" v-for="event in filteredEvents">
                    <td>
                        <strong>
                            {{ event.name }}
                        </strong>
                    </td>
                    <td class="right aligned collapsing">
                        <DownloadButton v-bind:url="schedule.exports.event_get + event.id + '/'" />
                        <sui-button class="actionbuttons" :loading="loadingModal" :disabled="loadingModal" size="small" color="blue" content="Alterar Palestrante" @click="changeSpeaker(event)" />
                        <sui-button class="actionbuttons" size="small" color="red" content="Apagar" @click="deleteEvent(event)" />
                    </td>
                </tr>
            </tbody>
        </table>
        <sui-modal v-model="showSpeakerModal" size="small">

                <sui-modal-header>Alterar palestrante de {{ selectedEvent.name }}</sui-modal-header>
                <sui-modal-content>
                    <sui-modal-description>
                        <p v-if="selectedEvent.speaker">O palestrante atual é {{ selectedEvent.speaker.full_name }} ({{ selectedEvent.speaker.email }})</p>
                        <p>Selecionar <span v-if="selectedEvent.speaker">outro </span>palestrante?</p>
                    </sui-modal-description>
                    <select id="speaker_modal" class="ui search selection dropdown" placeholder="Selecione alguém"></select>
                </sui-modal-content>
                <sui-modal-actions>
                    <sui-button content="Remover palestrante" negative labelPosition="right" icon="times" className="" @click="removeSpeaker(selectedEvent.id)" :loading="loadingButton" :disabled="loadingButton" v-if="selectedEvent.speaker" />
                    <sui-button content="Definir palestrante" positive labelPosition="right" icon="check" className="" @click="setSpeaker(selectedEvent.id)" :loading="loadingButton" :disabled="!selectedSpeaker || loadingButton" />
                </sui-modal-actions>
        </sui-modal>
    </div>
</template>

<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import swal from "sweetalert";
import { ModelSubscription } from "model_sockets/js/subscription";

import DownloadButton from "project/components/extra/download_button.vue";

export default {
    props: ["schedule_context"],
    components: { DownloadButton },
    data() {
        return {
            schedule: this.schedule_context,
            eventList: [],
            searchText: "",

            selectedEvent: {},
            showSpeakerModal: false,
            loadingModal: false,
            loadingButton: false,
            selectedSpeaker: {}
        };
    },
    computed: {
        filteredEvents() {
            return this.eventList.filter(event => {
                return (
                    event.name
                        .toLowerCase()
                        .indexOf(this.searchText.toLowerCase()) > -1
                );
            });
        }
    },
    methods: {
        getEventList() {
            var comp = this;
            axios
                .get(this.schedule.api.list_events)
                .then(function(data) {
                    comp.eventList = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        deleteEvent(event) {
            self = this;
            swal({
                title: "Apagar " + event.name + "?",
                text: "Não pode ser revertido!",
                dangerMode: true,
                icon: "warning",
                buttons: ["Cancelar", "Apagar"]
            }).then(apagar => {
                if (apagar) {
                    axios
                        .delete(self.schedule.api.delete_event + event.id + "/")
                        .then(data => {
                            toast("Atenção!", "Evento apagado", "info");
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
        eventUpdated(event) {
            let eventIdx = this.eventList.findIndex(obj => obj.id == event.id);
            this.eventList.splice(eventIdx, 1, event);
        },
        eventCreated(event) {
            this.eventList.push(event);
        },
        eventDeleted(event) {
            let eventIdx = this.eventList.findIndex(obj => obj.id == event.id);
            this.eventList.splice(eventIdx, 1);
        },
        changeSpeaker(event) {
            this.loadingModal = true;
            this.selectedEvent = {};
            var comp = this;
            axios
                .get(this.schedule.api.get_event + event.id + "/")
                .then(data => {
                    comp.selectedEvent = data.data;
                    comp.loadingModal = false;
                    comp.showSpeakerModal = true;
                    $("#speaker_modal").dropdown({
                        apiSettings: {
                            url:
                                comp.schedule.api.sui_list_profiles +
                                "?search={query}",
                            cache: false
                        },
                        filterRemoteData: false,
                        saveRemoteData: false,
                        onChange: function(value) {
                            comp.selectedSpeaker = value;
                        }
                    });
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        removeSpeaker(event_id) {
            var comp = this;
            this.loadingButton = true;
            axios.patch(this.schedule.api.get_event + event_id + '/', {
                speaker_unique_id: null
            })
            .then(data => {
                comp.showSpeakerModal = false;
                toast("Atenção!", "Palestrante removido", "info");
            })
            .catch(function(error) {
                console.error(error);
                toast("Opa!", "Algo de errado aconteceu :(", "error");
            })
            .then(d => {
                comp.loadingButton = false;
            })
        },
        setSpeaker(event_id) {
            var comp = this;
            this.loadingButton = true;
            axios.patch(this.schedule.api.get_event + event_id + '/', {
                speaker_unique_id: this.selectedSpeaker
            })
            .then(data => {
                comp.showSpeakerModal = false;
                toast("Sucesso!", "Palestrante alterado", "success");
            })
            .catch(function(error) {
                console.error(error);
                toast("Opa!", "Algo de errado aconteceu :(", "error");
            })
            .then(d => {
                comp.loadingButton = false;
            })
        },
    },
    mounted() {
        this.getEventList();

        var updatesub = new ModelSubscription("schedule", "Event", "update");
        var createsub = new ModelSubscription("schedule", "Event", "create");
        var deletesub = new ModelSubscription("schedule", "Event", "delete");
        updatesub.connect();
        createsub.connect();
        deletesub.connect();
        updatesub.subscribe(this.eventUpdated);
        createsub.subscribe(this.eventCreated);
        deletesub.subscribe(this.eventDeleted);
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
    font-size: 0.9em;
}
.ui.modal > .content {
    text-align: center;
}
</style>
