<template>
    <div class="tickets">
        <Ticket
        v-for="ticket in filteredTickets"
        v-bind:key="ticket.id"
        v-bind:ticket="ticket"
        v-bind:helper_context="helper"
        v-bind:user_context="user"
        @expired="ticketDeleted"
        @delete="deleteTicket"
        @claim="claimTicket"
        @complete="completeTicket"
        @reopen="reopenTicket" />
        <div v-if="filteredTickets.length == 0" class="ui segment">
            <div style="font-size: 4em; line-height: 1em">
                🙌
            </div>
            <br>
            Parece que não há tickets abertos!
        </div>
    </div>
</template>
<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import moment from "project/js/moment";
import { ModelSubscription } from "model_sockets/js/subscription";
import Ticket from "./ticket/ticket.vue";

export default {
    props: ["helper_context", "user_context"],
    components: { Ticket },
    data() {
        return {
            helper: this.helper_context,
            user: this.user_context,
            tickets: []
        };
    },
    computed: {
        filteredTickets() {
            var comp = this;
            return this.tickets.filter(
                ticket => ticket.state == 'open' && moment().isBefore(ticket.expires) || ticket.state == 'claimed'
            ).sort((a, b) => {
                // If a was claimed
                if (a.state == "claimed") {
                    // And the claimer is the current user
                    if (a.claimer.unique_id == comp.user.unique_id)
                        // Put it on top
                        return false;
                    // Else, put it on the bottom
                    return true;
                }
                // If b was claimed
                if (b.state == "claimed")
                    // And the claimer is the current user
                    if (b.claimer.unique_id == comp.user.unique_id)
                        // Put it on top
                        return true;
                    // Else, put it on the bottom
                    return false;
                // If none were claimed, sort by id
                return a.id > b.id;
            });
        }
    },
    methods: {
        getTickets() {
            var comp = this;
            axios
                .get(this.helper.api.list_tickets)
                .then(data => {
                    comp.tickets = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        ticketUpdated(ticket) {
            let ticketIdx = this.tickets.findIndex(obj => obj.id == ticket.id);
            if (ticketIdx >= 0) this.tickets.splice(ticketIdx, 1, ticket);
            else {
                this.tickets.push(ticket);
                this.tickets = this.tickets.slice(0);
            }
        },
        ticketDeleted(ticket) {
            let ticketIdx = this.tickets.findIndex(obj => obj.id == ticket.id);
            if (ticketIdx >= 0) this.tickets.splice(ticketIdx, 1);
        },
        deleteTicket(ticket) {
            axios.delete(this.helper.api.list_tickets + ticket.id + '/')
            .catch(function(error) {
                console.error(error);
                toast("Opa!", "Algo de errado aconteceu :(", "error");
            });
        },
        claimTicket(ticket) {
            axios.patch(this.helper.api.list_tickets + ticket.id + '/', {
                claimer_unique_id: this.user.unique_id
            })
            .catch(function(error) {
                console.error(error);
                toast("Opa!", "Algo de errado aconteceu :(", "error");
            });
        },
        completeTicket(ticket) {
            axios.patch(this.helper.api.list_tickets + ticket.id + '/', {
                set_completed: true
            })
            .catch(function(error) {
                console.error(error);
                toast("Opa!", "Algo de errado aconteceu :(", "error");
            });
        },
        reopenTicket(ticket) {
            axios.patch(this.helper.api.list_tickets + ticket.id + '/', {
                claimer_unique_id: null
            })
            .catch(function(error) {
                console.error(error);
                toast("Opa!", "Algo de errado aconteceu :(", "error");
            });
        },
    },
    mounted() {
        this.getTickets();
        var createsub = new ModelSubscription("helper", "Ticket", "create");
        var updatesub = new ModelSubscription("helper", "Ticket", "update");
        var deletesub = new ModelSubscription("helper", "Ticket", "delete");
        createsub.connect();
        updatesub.connect();
        deletesub.connect();
        createsub.subscribe(this.ticketUpdated);
        updatesub.subscribe(this.ticketUpdated);
        deletesub.subscribe(this.ticketDeleted);
    }
};
</script>
<style scoped>
.tickets {
    text-align: center;
}
</style>
