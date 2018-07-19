import Vue from 'vue'
import Dashboard from 'dashboard/components/dashboard/dashboard.vue'
import SuiVue from 'semantic-ui-vue'
import VueCookie from 'vue-cookie'

Vue.use(SuiVue);
Vue.use(VueCookie);

var base = new Vue({
    el: '#dashboard-app',
    data() {
        return {
            user_context: user_context,
            dashboard_context: dashboard_context,
            settings_context: settings_context,
            sidebar_context: sidebar_context
        }
    },
    template: '<Dashboard v-bind:sidebar_context="sidebar_context" v-bind:settings_context="settings_context" v-bind:dashboard_context="dashboard_context" v-bind:user_context="user_context" />',
    components: { Dashboard }
})
