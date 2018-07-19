import Vue from "vue";
import SuiVue from "semantic-ui-vue";
import Login from "project/components/login/login.vue";

Vue.use(SuiVue);

var login = new Vue({
    el: "#login-app",
    data() {
        return {
            login_context: login_context
        };
    },
    template: '<Login v-bind:login_context="login_context" />',
    components: { Login }
});
