<template>
    <div>
        <sui-card-group :items-per-row="3" stackable>
            <Event v-for="event in filteredEventList"
            v-bind:key="event.id"
            v-bind:event="event"
            @event-selected="$emit('event-selected', $event)" />
        </sui-card-group>

        <LoadingCards v-if="loadingData" />
    </div>
</template>

<script>
    import axios from 'project/js/axios_csrf'
    import toast from 'project/js/notifications'
    import swal from 'sweetalert'
    import Event from './event.vue'
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
                return this.eventList.slice(0).sort((event1, event2) => {
                    return moment(event1.start).isAfter(event2.start);
                }).filter(event => {
                    let duration = moment(event.duration, "HH:mm:ss");
                    let eventEnd = moment(event.start);
                    eventEnd = eventEnd.add(duration.format('HH'), 'hours').add(duration.format('mm'), 'minutes');
                    return moment().isBefore(eventEnd);
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
                axios.get(this.schedule.api.checkinable_events)
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
            }
        },
        mounted: function () {
            this.firstLoad();

            var updatesub = new ModelSubscription('schedule', 'Event', 'update');
            var createsub = new ModelSubscription('schedule', 'Event', 'create');
            var deletesub = new ModelSubscription('schedule', 'Event', 'delete');
            updatesub.connect();
            createsub.connect();
            deletesub.connect();
            updatesub.subscribe(this.getEventList);
            createsub.subscribe(this.getEventList);
            deletesub.subscribe(this.eventDeleted);
        }
    }
</script>
