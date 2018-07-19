import Vue from "vue";
import Sidebar from "project/components/sidebar/sidebar.vue";
import SuiVue from "semantic-ui-vue";

Vue.use(SuiVue);

var base = new Vue({
    el: "#sidebar-app",
    data() {
        return {
            sidebar_context: sidebar_context,
            user_context: user_context
        };
    },
    template:
        '<Sidebar v-bind:user_context="user_context" v-bind:sidebar_context="sidebar_context" />',
    components: { Sidebar }
});
