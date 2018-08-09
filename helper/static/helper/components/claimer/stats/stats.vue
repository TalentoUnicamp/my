<template>
    <div class="ui segment">
        <template v-if="mentorsAvailable">
            <div class="ui green empty circular label"
            style="margin-right: 4px"></div>
            <strong>{{ mentorsAvailable }}</strong> {{ mentorText }} online.
            Espera estimada: <strong>{{ estimatedWait }}</strong>
        </template>
        <template v-else>
            <div class="ui red empty circular label"
            style="margin-right: 4px"></div>
            Nenhum mentor online agora
        </template>
    </div>
</template>
<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import moment from "project/js/moment";
import * as math from "mathjs";
import { ModelSubscription } from "model_sockets/js/subscription";

export default {
    props: ["helper_context"],
    data() {
        return {
            helper: this.helper_context,
            onlineMentors: [],
            ticketList: []
        };
    },
    computed: {
        mentorsAvailable() {
            return this.onlineMentors.length;
        },
        mentorText() {
            if (this.mentorsAvailable == 1) return "mentor";
            return "mentores";
        },
        claimedTickets() {
            return this.ticketList.filter(ticket => ticket.claimed);
        },
        calcEstimatedWait() {
            let mentors = this.onlineMentors;
            let tickets = this.ticketList;
            let openTickets = this.ticketList.filter(ticket => {
                return !ticket.claimed && moment().isBefore(ticket.expires);
            });
            let claimedTickets = this.claimedTickets;
            // Median complete time
            let completedTickets = this.ticketList.filter(
                ticket => ticket.completed
            );
            let estCompletion;
            if (completedTickets.length) {
                estCompletion = math.median(
                    completedTickets.map(ticket =>
                        this.timeDiff(ticket.completed, ticket.claimed)
                    )
                )
            }
            let estResponse = math.median(claimedTickets.map(ticket => this.timeDiff(ticket.claimed, ticket.created)))
            if (mentors.length) {
                // If there are more mentors than tickets, return the median response time
                if (mentors.length > openTickets.length || !completedTickets.length) {
                    return estResponse;
                } else {
                    // There are a lot of tickets open
                    // mentors have to finish their tickets before taking new ones
                    let now = moment().unix();
                    // Latest open ticket
                    let latestOpen = math.max(openTickets.map(ticket => moment(ticket.created).unix()));
                    if (claimedTickets.length) {
                        let earliestClaimed = math.min(claimedTickets.map(ticket => moment(ticket.claimed).unix()));
                        // Take the minimum between:
                        // - The claim time is similar between the latest ticket and a future one
                        // - The first unclaimed ticket is close to being completed
                        return math.min((now - latestOpen + estResponse + estCompletion), (now - earliestClaimed + estResponse + estCompletion));
                    } else {
                        return now - latestOpen + estResponse;
                    }
                }
            }
        },
        estimatedWait() {
            if (!this.claimedTickets.length)
                return "sem dados";
            return this.formatTime(this.calcEstimatedWait);
        }
    },
    methods: {
        timeDiff(timea, timeb) {
            return moment
                .duration(moment(timea).diff(moment(timeb)))
                .asSeconds();
        },
        formatTime(seconds) {
            let output = (seconds % 60).toFixed(0) + " segundos";
            if (seconds > 60) {
                let out = Math.floor(seconds / 60);
                let txt = out == 1 ? " minuto, " : " minutos, ";
                output = out + txt + output;
            }
            if (seconds > 3600) {
                let out = Math.floor(seconds / 3600);
                let txt = out == 1 ? " hora, " : " horas, ";
                output = out + txt + output;
            }
            return output;
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
            else if (mentor.online){
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
        },
        getTicketList() {
            var comp = this;
            axios
                .get(this.helper.api.list_tickets)
                .then(data => {
                    comp.ticketList = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        ticketUpdated(ticket) {
            let ticketIdx = this.ticketList.findIndex(
                obj => obj.id == ticket.id
            );
            if (ticketIdx >= 0) this.ticketList.splice(ticketIdx, 1, ticket);
            else {
                this.ticketList.push(ticket);
                this.ticketList = this.ticketList.slice(0);
            }
        },
        ticketDeleted(ticket) {
            let ticketIdx = this.ticketList.findIndex(
                obj => obj.id == ticket.id
            );
            if (ticketIdx >= 0) this.ticketList.splice(ticketIdx, 1);
        }
    },
    mounted() {
        this.getOnlineMentorsList();
        this.getTicketList();

        var updatesub = new ModelSubscription("helper", "Mentor", "update");
        var deletesub = new ModelSubscription("helper", "Mentor", "delete");
        updatesub.connect();
        deletesub.connect();
        updatesub.subscribe(this.mentorUpdated);
        deletesub.subscribe(this.mentorDeleted);

        var createsub2 = new ModelSubscription("helper", "Ticket", "create");
        var updatesub2 = new ModelSubscription("helper", "Ticket", "update");
        var deletesub2 = new ModelSubscription("helper", "Ticket", "delete");
        createsub2.connect();
        updatesub2.connect();
        deletesub2.connect();
        createsub2.subscribe(this.ticketUpdated)
        updatesub2.subscribe(this.ticketUpdated);
        deletesub2.subscribe(this.ticketDeleted);
    }
};
</script>
<style scoped>
</style>
