import Vue from "vue";
import Staff from "staff/components/staff.vue";
import SuiVue from "semantic-ui-vue";

Vue.use(SuiVue);

var base = new Vue({
    data() {
        return {
            staff_context: staff_context
        };
    },
    el: "#staff-app",
    template: '<Staff v-bind:staff_context="staff_context" />',
    components: { Staff }
});
