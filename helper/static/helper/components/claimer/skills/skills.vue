<template>
    <div class="ui blue segment">
        <div class="ui dividing header">
            Habilidades dos Mentores
        </div>
        <div class="ui container">
            <div class="ui label"
            v-bind:key="skill[0]" v-for="skill in skillList">{{ skill[0] }} - {{ skill[1] }}</div>
        </div>
    </div>
</template>
<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import { ModelSubscription } from "model_sockets/js/subscription";

export default {
    props: ["helper_context"],
    data() {
        return {
            helper: this.helper_context,
            onlineMentors: []
        };
    },
    computed: {
        skillList() {
            let skills = this.flatten(
                this.onlineMentors
                    .map(mentor => JSON.parse(mentor.skills))
                    .filter(skills => skills.length)
            );
            let countVector = {};
            for (let vector in skills) {
                let term = skills[vector];
                if (countVector[term] === undefined) countVector[term] = 1;
                else countVector[term]++;
            }
            return Object.entries(countVector);
        }
    },
    methods: {
        flatten(arr) {
            let comp = this;
            return arr.reduce(function(flat, toFlatten) {
                return flat.concat(
                    Array.isArray(toFlatten)
                        ? comp.flatten(toFlatten)
                        : toFlatten
                );
            }, []);
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
            else if (mentor.online) {
                this.onlineMentors.push(mentor);
                this.onlineMentors = this.onlineMentors.slice(0);
            }
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
        this.getOnlineMentorsList();

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
.ui.label {
    margin-bottom: 10px;
}
</style>
