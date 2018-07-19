import Vue from "vue";
import settingssub from "project/js/settings_subscriptions";

var sub = new Vue({
    el: "#settingssub-app",
    data() {
        return {
            settings_context: settings_context,
            sub: settingssub
        };
    },
    methods: {
        updateSettings(data) {
            for (let key in data) this.settings_context[key] = data[key];
        }
    },
    mounted() {
        this.sub.subscribe(this.updateSettings);
    },
    template: ""
});
