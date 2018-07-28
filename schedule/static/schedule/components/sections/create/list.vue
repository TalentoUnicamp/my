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
                <div class="sixteen wide field">
                    <div class="ui left icon fluid input">
                        <i class="search icon"></i>
                        <input type="text" class="searchText" placeholder="Pesquisar..." v-model="searchText">
                    </div>
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
                        <sui-button class="actionbuttons" size="small" color="red" content="Apagar" @click="deleteEvent(event)" />
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import axios from 'project/js/axios_csrf'
    import toast from 'project/js/notifications'
    import swal from 'sweetalert'
    import { ModelSubscription } from 'model_sockets/js/subscription'

    export default {
        props: ["schedule_context"],
        data() {
            return {
                schedule: this.schedule_context,
                eventList: [],
                searchText: '',
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
                axios.get(this.schedule.api.list_events)
                .then(function (data) {
                    comp.eventList = data.data;
                })
                .catch(function (error) {
                    console.error(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            },
            deleteEvent(event) {
                self = this;
                swal({
                    title: 'Apagar ' + event.name + '?',
                    text: 'Não pode ser revertido!',
                    dangerMode: true,
                    icon: 'warning',
                    buttons: ["Cancelar", "Apagar"]
                })
                .then(apagar => {
                    if (apagar) {
                        axios.delete(self.schedule.api.delete_event + event.id + '/')
                        .then(data => {
                            toast('Atenção!', 'Evento apagado', 'info');
                        })
                        .catch(function (error) {
                            console.error(error);
                            toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                        });
                    }
                })
            },
            eventUpdated(event) {
                let eventIdx = this.eventList.findIndex((obj => obj.id == event.id));
                this.eventList.splice(eventIdx, 1, event);
            },
            eventCreated(event) {
                this.eventList.push(event);
            },
            eventDeleted(event) {
                let eventIdx = this.eventList.findIndex((obj => obj.id == event.id));
                this.eventList.splice(eventIdx, 1);
            },
        },
        mounted() {
            this.getEventList();

            var updatesub = new ModelSubscription('schedule', 'Event', 'update');
            var createsub = new ModelSubscription('schedule', 'Event', 'create');
            var deletesub = new ModelSubscription('schedule', 'Event', 'delete');
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
</style>
