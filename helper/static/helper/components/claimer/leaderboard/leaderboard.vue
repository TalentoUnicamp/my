<template>
    <div class="ui segment yellow">
        <h3 class="ui dividing header">
            Placar
        </h3>
        <div class="ui large relaxed ordered list">
            <Mentor v-for="mentor in rankedMentors" :key="mentor.id" :mentor="mentor" />
        </div>
    </div>
</template>
<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import { ModelSubscription } from "model_sockets/js/subscription";
import Mentor from "./mentor/mentor.vue";

export default {
    props: ["helper_context"],
    components: { Mentor },
    data() {
        return {
            helper: this.helper_context,
            mentors: []
        };
    },
    computed: {
        filteredMentors() {
            return this.mentors.filter(mentor => {
                return mentor.claimed_tickets.filter(
                    ticket => ticket.state == "completed"
                ).length;
            });
        },
        rankedMentors() {
            return this.filteredMentors
                .map(mentor => {
                    mentor["rank"] = this.laplaceSmooth(
                        mentor.claimed_tickets
                            .filter(ticket => ticket.state == "completed")
                            .map(ticket => ticket.rating)
                    );
                    return mentor;
                })
                .sort((a, b) => a.rank < b.rank);
        }
    },
    methods: {
        laplaceSmooth(list) {
            let alpha = 6,
                beta = 2,
                sum = list.reduce((a, b) => a + b, 0);
            return ((sum + alpha) / (list.length + beta)).toFixed(1);
        },
        getMentorsList() {
            var comp = this;
            axios
                .get(this.helper.api.list_mentors)
                .then(data => {
                    comp.mentors = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        mentorUpdated(mentor) {
            let mentorIdx = this.mentors.findIndex(obj => obj.id == mentor.id);
            // If mentor in the list
            if (mentorIdx >= 0) {
                // And update is online, update it
                if (mentor.online) this.mentors.splice(mentorIdx, 1, mentor);
                // If offline, remove it
                else this.mentors.splice(mentorIdx, 1);
            }
            // If is not on list, and online, push it
            else if (mentor.online) {
                this.mentors.push(mentor);
                this.mentors = this.mentors.slice(0);
            }
            // Ignore if not on list and offline
        },
        mentorDeleted(mentor) {
            let mentorIdx = this.mentors.findIndex(obj => obj.id == mentor.id);
            // If deleted and on list, remove it
            if (mentorIdx >= 0) this.mentors.splice(mentorIdx, 1);
        }
    },
    mounted() {
        this.getMentorsList();
        var updatesub = new ModelSubscription("helper", "Mentor", "update");
        var deletesub = new ModelSubscription("helper", "Mentor", "delete");
        updatesub.connect();
        deletesub.connect();
        updatesub.subscribe(this.mentorUpdated);
        deletesub.subscribe(this.mentorDeleted);
    }
};
</script>
<style scoped>
.ui.large.list {
    font-size: 1.1em;
}
</style>
