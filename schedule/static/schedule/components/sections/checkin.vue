<template>
    <div>
        <br>
        <div>
            <h2 class="ui header centered">
                <div class="content">
                    Check-in em eventos
                    <div class="sub header">Use essa tela para fazer o check-in de participantes em eventos<br>Apenas participantes que fazem check-in podem dar feedback!</div>
                </div>
            </h2>
        </div>
        <br>
        <List
        v-if="!selectedEvent"
        :schedule_context="schedule"
        @event-selected="eventSelected" />
        <CheckIn
        v-if="selectedEvent"
        :schedule_context="schedule"
        :event="selectedEvent"
        @go-back="goBack" />
    </div>
</template>

<script>
import CheckIn from './checkin/checkin.vue'
import List from './checkin/list.vue'

export default {
    props: ["schedule_context"],
    components: { CheckIn, List },
    data() {
        return {
            schedule: this.schedule_context,
            selectedEvent: null
        }
    },
    methods: {
        eventSelected(event) {
            this.selectedEvent = event;
        },
        goBack() {
            this.selectedEvent = null;
        }
    }
};
</script>
