import Vue from "vue";
import selfsub from "project/js/self_subscriptions";

var sub = new Vue({
    el: "#selfsub-app",
    data() {
        return {
            sidebar_context: sidebar_context,
            user_context: user_context,
            sub: selfsub
        };
    },
    methods: {
        updateUser(data) {
            // let map = {
            //     state: 'state',
            //     is_admin: 'is_admin',
            //     is_hacker: 'is_hacker',
            //     is_staff: 'is_staff',
            //     unique_id: 'unique_id',
            //     token: 'token',
            //     is_verified: 'is_verified',
            //     email: 'email'
            // }
            for (let key in data) this.user_context[key] = data[key];

        }
    },
    mounted() {
        this.sub.subscribe(this.updateUser);
    },
    template: ""
});
