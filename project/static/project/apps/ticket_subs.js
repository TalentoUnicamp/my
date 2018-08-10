import Vue from "vue";
import toast from "project/js/notifications";
import subs from "project/js/ticket_subscriptions";

var sub = new Vue({
    el: "#ticketsub-app",
    data() {
        return {
            sidebar: sidebar_context,
            user: user_context,
            subs: subs,
            currentTicket: null,
            connected: false
        };
    },
    watch: {
        user() {
            this.loadConnections();
        }
    },
    methods: {
        ticketCreated(ticket) {
            this.currentTicket = ticket;
        },
        ticketUpdated(ticket) {
            if (
                this.currentTicket.state == "open" &&
                ticket.state == "claimed"
            ) {
                // Ticket was claimed
                toast(
                    "Ticket pego",
                    ticket.claimer.full_name + " pegou seu ticket!",
                    "success"
                );
            }
            if (
                this.currentTicket.state == "claimed" &&
                ticket.state == "open"
            ) {
                // Ticket was claimed
                toast(
                    "Ticket reaberto",
                    this.currentTicket.claimer.full_name +
                        " reabriu seu ticket",
                    "info"
                );
            }
            if (
                this.currentTicket.state == "claimed" &&
                ticket.state == "unrated"
            ) {
                // Ticket was completed
                toast(
                    "Ticket finalizado",
                    "Não esqueça de avaliar " + ticket.claimer.full_name,
                    "success"
                );
            }
            this.currentTicket = ticket;
        },
        loadConnections() {
            // Only connect if the current tab is not helper
            if (this.connected) {
                this.subs.create.disconnect();
                this.subs.update.disconnect();
            }
            if (
                this.sidebar.active_tab != "helper" &&
                (this.user.employee_company_access >= 0 || this.user.is_mentor)
            ) {
                this.subs.create.connect();
                this.subs.update.connect();
                this.subs.create.subscribe(this.ticketCreated);
                this.subs.update.subscribe(this.ticketUpdated);
                this.connected = true;
            } else {
                this.connected = false;
            }
        }
    },
    mounted() {
        this.loadConnections();
    },
    template: ""
});
