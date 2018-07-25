import Vue from "vue";
import Stats from "stats/components/stats.vue";
import SuiVue from "semantic-ui-vue";

Vue.use(SuiVue);

var base = new Vue({
    data() {
        return {
            stats_context: stats_context,
            user_context: user_context
        };
    },
    el: "#stats-app",
    template: '<Stats v-bind:stats_context="stats_context" v-bind:user_context="user_context" />',
    components: { Stats }
});
