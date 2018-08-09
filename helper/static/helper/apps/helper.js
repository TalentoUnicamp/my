import Vue from "vue";
import Helper from "helper/components/helper.vue";
import SuiVue from "semantic-ui-vue";

Vue.use(SuiVue);

var base = new Vue({
    data() {
        return {
            helper_context: helper_context,
            user_context: user_context,
            settings_context: settings_context,
        };
    },
    el: "#helper-app",
    template: '<Helper v-bind:helper_context="helper_context" v-bind:user_context="user_context" :settings_context="settings_context" />',
    components: { Helper }
});
