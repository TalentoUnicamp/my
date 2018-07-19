<template>
    <div>
        <br>
        <div class="small title">
            Lista de hackers
        </div>
        <HackerTable
        v-bind:staff_context="staff"
        v-bind:data="hackerList" />
    </div>
</template>

<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import HackerTable from "./hacker_table.vue";

import { ModelSubscription } from "model_sockets/js/subscription";

export default {
    components: { HackerTable },
    props: ["staff_context"],
    data() {
        return {
            staff: this.staff_context,
            hackerList: [],
            allowedStates: [
                "checkedin",
                "confirmed",
                "waitlist",
                "admitted",
                "submitted",
                "declined"
            ]
        };
    },
    methods: {
        getUserList() {
            self = this;
            axios
                .get(this.staff.api.list_hacker_profiles)
                .then(function(data) {
                    self.hackerList = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        hackerStateAllowed(hacker) {
            return this.allowedStates.indexOf(hacker.state) > -1;
        },
        userUpdated(user) {
            if (!this.hackerStateAllowed(user)) return this.userDeleted(user);
            let userIdx = this.hackerList.findIndex(
                obj => obj.unique_id == user.unique_id
            );
            if (userIdx == -1) return this.userCreated(user);
            this.hackerList.splice(userIdx, 1, user);
        },
        userCreated(user) {
            if (!this.hackerStateAllowed(user)) return;
            this.hackerList.push(user);
        },
        userDeleted(user) {
            let userIdx = this.hackerList.findIndex(
                obj => obj.unique_id == user.unique_id
            );
            if (userIdx > -1) this.hackerList.splice(userIdx, 1);
        }
    },
    mounted: function() {
        this.getUserList();

        var updatesub = new ModelSubscription(
            "user_profile",
            "Profile",
            "update"
        );
        var createsub = new ModelSubscription(
            "user_profile",
            "Profile",
            "create"
        );
        var deletesub = new ModelSubscription(
            "user_profile",
            "Profile",
            "delete"
        );
        updatesub.connect();
        createsub.connect();
        deletesub.connect();
        updatesub.subscribe(this.userUpdated);
        createsub.subscribe(this.userCreated);
        deletesub.subscribe(this.userDeleted);
    }
};
</script>
