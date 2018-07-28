import Vue from "vue";
import Schedule from "schedule/components/schedule.vue";
import SuiVue from "semantic-ui-vue";

Vue.use(SuiVue);

var base = new Vue({
    data() {
        return {
            schedule_context: schedule_context,
            user_context: user_context
        }
    },
    el: "#schedule-app",
    template: '<Schedule v-bind:schedule_context="schedule_context" v-bind:user_context="user_context" />',
    components: { Schedule }
});
