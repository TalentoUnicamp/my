import Vue from "vue";
import Company from "company/components/company.vue";
import SuiVue from "semantic-ui-vue";

Vue.use(SuiVue);

var base = new Vue({
    data() {
        return {
            company_context: company_context
        };
    },
    el: "#company-app",
    template: '<Company v-bind:company_context="company_context" />',
    components: { Company }
});
