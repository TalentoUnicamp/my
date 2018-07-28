<template>
    <div>
        <br>
        <div>
            <h2 class="ui header centered">
                <div class="content">
                    Seus eventos
                    <div class="sub header">Esses são os seus eventos<br>Aqui você pode editá-los e ver detalhes como o feedback de participantes</div>
                </div>
            </h2>
        </div>
        <br>
        <List
        v-if="action == 'list_events'"
        :schedule_context="schedule"
        :event="selectedEvent"
        @see-details="seeDetails"
        @edit-event="editEvent" />
        <Edit
        v-if="action == 'edit_event'"
        :schedule_context="schedule"
        :event="selectedEvent"
        @go-back="goBack" />
        <Detail
        v-if="action == 'detail_event'"
        :schedule_context="schedule"
        :event="selectedEvent"
        @go-back="goBack" />
    </div>
</template>

<script>
import Edit from './my/edit.vue'
import Detail from './my/details.vue'
import List from './my/list.vue'

export default {
    props: ["schedule_context"],
    components: { Edit, List, Detail },
    data() {
        return {
            schedule: this.schedule_context,
            selectedEvent: null,
            action: 'list_events',
        }
    },
    methods: {
        eventSelected(event) {
            this.selectedEvent = event;
        },
        goBack() {
            this.selectedEvent = null;
            this.action = 'list_events';
        },
        seeDetails(event) {
            this.selectedEvent = event;
            this.action = 'detail_event';
        },
        editEvent(event) {
            this.selectedEvent = event;
            this.action = 'edit_event';
        }
    }
};
</script>
