import Vue from "vue";
import Admin from "godmode/components/admin.vue";
import SuiVue from "semantic-ui-vue";

Vue.use(SuiVue);

var admin = new Vue({
    data() {
        return {
            admin_context: admin_context,
            settings_context: settings_context
        };
    },
    el: "#admin-app",
    template:
        '<Admin v-bind:admin_context="admin_context" v-bind:settings_context="settings_context" />',
    components: { Admin }
});
