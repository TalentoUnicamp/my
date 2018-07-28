<template>
    <div>
        <br>
        <div>
            <h2 class="ui header centered">
                <div class="content">
                    Eventos disponíveis
                    <div class="sub header">Esses são os eventos disponíveis no momento<br>Sinta-se livre para se inscrever e participar de todos!</div>
                </div>
            </h2>
        </div>
        <br>
        <sui-card-group :items-per-row="3" stackable>
            <Event v-for="event in filteredEventList"
            v-bind:key="event.id"
            v-bind:event="event"
            @attend-event="attendEvent" />
        </sui-card-group>

        <LoadingCards v-if="loadingData" />
    </div>
</template>

<script>
    import axios from 'project/js/axios_csrf'
    import toast from 'project/js/notifications'
    import swal from 'sweetalert'
    import Event from './all/event.vue'
    import LoadingCards from 'schedule/components/loading_cards.vue'

    import moment from 'project/js/moment'

    import { ModelSubscription } from 'model_sockets/js/subscription'

    export default {
        components: { Event, LoadingCards },
        props: ['schedule_context'],
        data() {
            return {
                schedule: this.schedule_context,
                eventList: [],

                loadingData: false
            }
        },
        filters: {
            calendar(date) {
                return moment(date).calendar();
            }
        },
        computed: {
            filteredEventList() {
                return this.eventList.filter(event => {
                    // Only show events in the future (don't include started events)
                    return moment().isBefore(event.start);
                }).sort((event1, event2) => {
                    return moment(event1.start).isAfter(event2.start);
                })
            }
        },
        methods: {
            firstLoad(event) {
                this.loadingData = true;
                this.getEventList();
            },
            getEventList(event) {
                let self = this;
                axios.get(this.schedule.api.not_registered_list_events)
                .then(data => {
                    self.eventList = data.data;
                })
                .catch(error => {
                    console.log(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                })
                .then(data => {
                    self.loadingData = false;
                })
            },
            eventDeleted(event) {
                let eventIdx = this.eventList.findIndex((obj => obj.id == event.id));
                if (eventIdx >= 0)
                    this.eventList.splice(eventIdx, 1);
            },
            attendEvent(event_id) {
                axios.post(this.schedule.api.attend_event, {
                    event_id: event_id
                })
                .then(data => {
                    toast('Pronto!', 'Evento movido para a aba "Atenderei"', 'success');
                })
                .catch(error => {
                    console.log(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            }
        },
        mounted: function () {
            this.firstLoad();

            var updatesub = new ModelSubscription('schedule', 'Event', 'update');
            var createsub = new ModelSubscription('schedule', 'Event', 'create');
            var deletesub = new ModelSubscription('schedule', 'Event', 'delete');
            var m2maddsub = new ModelSubscription('schedule', 'Event', 'm2m_add');
            var m2mremovesub = new ModelSubscription('schedule', 'Event', 'm2m_remove');
            var m2mclearsub = new ModelSubscription('schedule', 'Event', 'm2m_clear');
            updatesub.connect();
            createsub.connect();
            deletesub.connect();
            m2maddsub.connect();
            m2mremovesub.connect();
            m2mclearsub.connect();
            updatesub.subscribe(this.getEventList);
            createsub.subscribe(this.getEventList);
            deletesub.subscribe(this.eventDeleted);
            m2maddsub.subscribe(this.getEventList);
            m2mclearsub.subscribe(this.getEventList);
            m2mclearsub.subscribe(this.getEventList);
        }
    }
</script>
