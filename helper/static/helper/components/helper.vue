<template>
    <div id="staff" class="page">
        <div class="divided title">
            Helper
        </div>

        <div class="ui stackable centered page grid">
            <LatestAnnouncement />
            <div class="row">
                <div class="column">
                    <sui-menu v-if="user.is_mentor" class="stackable three item">
                        <a
                        is="sui-menu-item"
                        v-for="item in items"
                        :active="isActive(item)"
                        :key="item"
                        :content="item"
                        @click="select(item)"
                        />
                    </sui-menu>

                    <Sender
                    v-bind:helper_context="helper"
                    v-bind:user_context="user"
                    v-bind:settings_context="settings"
                    v-show="isActive('Abrir Ticket')" />
                    <Claimer
                    v-if="user.is_mentor"
                    v-bind:helper_context="helper"
                    v-bind:user_context="user"
                    v-show="isActive('Pegar Ticket')" />
                    <Profile
                    v-if="user.is_mentor && isActive('Perfil')"
                    v-bind:helper_context="helper" />

                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import Sender from "./sender/sender.vue";
import Claimer from "./claimer/claimer.vue";
import Profile from "./profile/profile.vue";
import LatestAnnouncement from "announcement/components/latest_announcement.vue";
import MentorSubscription from "helper/js/mentor_sub";
import { ModelSubscription } from "model_sockets/js/subscription";

export default {
    props: ["helper_context", "user_context", "settings_context"],
    components: { Sender, Claimer, Profile, LatestAnnouncement },
    data() {
        return {
            helper: this.helper_context,
            user: this.user_context,
            settings: this.settings_context,
            onlineMentors: [],
            active: "Abrir Ticket",
            items: ["Abrir Ticket", "Pegar Ticket", "Perfil"]
        };
    },
    methods: {
        isActive(name) {
            return this.active === name;
        },
        select(name) {
            this.active = name;
        },
        getOnlineMentorsList() {
            var comp = this;
            axios
                .get(this.helper.api.online_mentors)
                .then(data => {
                    comp.onlineMentors = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        mentorUpdated(mentor) {
            let mentorIdx = this.onlineMentors.findIndex(
                obj => obj.id == mentor.id
            );
            // If mentor in the list
            if (mentorIdx >= 0) {
                // And update is online, update it
                if (mentor.online)
                    this.onlineMentors.splice(mentorIdx, 1, mentor);
                // If offline, remove it
                else this.onlineMentors.splice(mentorIdx, 1);
            }
            // If is not on list, and online, push it
            else if (mentor.online) this.onlineMentors.push(mentor);
            // Ignore if not on list and offline
        },
        mentorDeleted(mentor) {
            let mentorIdx = this.onlineMentors.findIndex(
                obj => obj.id == mentor.id
            );
            // If deleted and on list, remove it
            if (mentorIdx >= 0) this.onlineMentors.splice(mentorIdx, 1);
        }
    },
    mounted() {
        let mentorsub = new MentorSubscription();
        if (this.user.is_mentor) {
            // Delay connection by a bit
            setTimeout(() => {
                mentorsub.connect();
            }, 2000);
        }
    }
};
</script>
