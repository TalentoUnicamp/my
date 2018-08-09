<template>
    <div class="ticketPanel">
        <div class="ui segment">
            <template v-if="queueEnabled">
                <template v-if="currentTicket && !isExpired">
                    <template v-if="ticketStatus == 'open' || ticketStatus == 'claimed'">
                        <template v-if="ticketStatus == 'open'">
                            <div class="title">
                                Seu ticket está aberto
                            </div>
                            <div class="content">
                                <p>
                                    Te avisaremos quando ele for pego!
                                </p>
                                <p v-if="ticketExpires">
                                    <!-- Se ele expirar -->
                                    Seu ticket vai expirar {{ expiresIn }}
                                </p>
                            </div>
                        </template>
                        <template v-else-if="ticketStatus == 'claimed'">
                            <div class="title">
                                Seu ticket foi pego!
                            </div>
                            <div class="content">
                                {{ currentTicket.claimer.full_name }} pegou seu ticket
                                <br>
                                Ele(a) já está a caminho!
                            </div>
                        </template>

                        <br>

                        <sui-button
                        fluid
                        negative
                        content="Deixa pra lá!"
                        v-bind:disabled="loadingButton"
                        v-bind:loading="loadingButton"
                        @click="nevermind" />
                    </template>

                    <template v-else-if="ticketStatus == 'unrated'">
                        <Feedback v-bind:helper_context="helper" v-bind:ticket="currentTicket" />
                    </template>
                </template>
                <template v-else>
                    <div class="title">
                        <p>
                            <strong>
                                Olá, {{ user.first_name }}!
                            </strong>
                        </p>
                        Como posso te ajudar?
                    </div>
                    <div class="content">
                        Eu preciso de ajuda com
                        <br>
                        <input class="clean" placeholder="descreva seu problema"
                        v-model="topic">
                        <br>
                        você pode me encontrar em
                        <br>
                        <input class="clean" placeholder="mesa x / perto da entrada"
                        v-model="location">
                        <br>
                        e pode entrar em contato comigo através de
                        <br>
                        <input class="clean" placeholder="seu telefone / grite meu nome"
                        v-model="contact">
                    </div>
                    <br>
                    <sui-button
                    fluid
                    positive
                    v-bind:disabled="!(topic && location && contact) || loadingButton"
                    v-bind:loading="loadingButton"
                    content="Me ajuda!"
                    @click="submitTicket" />
                </template>
            </template>
            <template v-else>
                A fila está fechada!
            </template>
        </div>
    </div>
</template>
<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import moment from "project/js/moment";
import Feedback from "helper/components/sender/feedback/feedback.vue";
import TicketSubscription from "helper/js/ticket_sub.js";

export default {
    props: ["helper_context", "user_context", "settings_context"],
    components: { Feedback },
    data() {
        return {
            helper: this.helper_context,
            user: this.user_context,
            settings: this.settings_context,
            currentTicket: null,
            expiresIn: null,
            expireCounter: null,
            loadingButton: false,
            topic: "",
            location: "",
            contact: "",
            firstLoad: false
        };
    },
    watch: {
        currentTicket(val) {
            if (this.currentTicket) {
                this.scheduleCounter();
                if (this.currentTicket.state == "completed")
                    this.currentTicket = null;
            } else {
                this.stopCounter();
            }
        }
    },
    computed: {
        ticketStatus() {
            return this.currentTicket.state;
        },
        ticketExpires() {
            let far = moment().add(11, "months");
            return moment(this.currentTicket.expires).isBefore(far);
        },
        isExpired() {
            // Force recalc on update
            if (this.currentTicket.state == "expired") return true;
            if (this.currentTicket.state != "open") return false;
            this.expiresIn + "load";
            return moment().isAfter(this.currentTicket.expires);
        },
        queueEnabled() {
            return this.settings.ticket_queue_open && this.firstLoad;
        }
    },
    methods: {
        getCurrentTicket() {
            var comp = this;
            axios
                .get(this.helper.api.last_ticket)
                .then(data => {
                    if ($.isEmptyObject(data.data)) comp.currentTicket = null;
                    else {
                        comp.currentTicket = data.data;
                    }
                    comp.firstLoad = true;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        submitTicket() {
            var comp = this;
            this.loadingButton = true;
            axios
                .post(this.helper.api.list_tickets, {
                    topic: this.topic,
                    location: this.location,
                    contact: this.contact
                })
                .then(data => {
                    comp.topic = "";
                    comp.location = "";
                    comp.contact = "";
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                })
                .then(data => {
                    comp.loadingButton = false;
                });
        },
        nevermind() {
            var comp = this;
            this.loadingButton = true;
            axios
                .delete(
                    this.helper.api.list_tickets + this.currentTicket.id + "/"
                )
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                })
                .then(data => {
                    comp.loadingButton = false;
                });
        },
        getExpiresIn() {
            if (this.currentTicket)
                this.expiresIn = moment(this.currentTicket.expires).fromNow();
        },
        startCounter() {
            this.expireCounter = setInterval(() => {
                this.getExpiresIn();
            });
        },
        stopCounter() {
            if (this.expireCounter) {
                clearInterval(this.expireCounter);
                this.expireCounter = null;
                this.expiresIn = null;
            }
        },
        scheduleCounter() {
            if (this.currentTicket) {
                this.stopCounter();
                this.getExpiresIn();
                let expire_seconds = moment(
                    this.currentTicket.expires
                ).seconds();
                let now_seconds = moment().seconds();
                let diff = expire_seconds - now_seconds;
                let sch = diff >= 0 ? diff : 60 + diff;
                setTimeout(() => {
                    this.startCounter();
                }, (sch + 1) * 1000);
            }
        },
        ticketCreated(ticket) {
            this.currentTicket = ticket;
            this.scheduleCounter();
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
            this.scheduleCounter();
        },
        ticketDeleted(ticket) {
            this.getCurrentTicket();
        }
    },
    mounted() {
        this.getCurrentTicket();
        let createsub = new TicketSubscription(this.user.unique_id, "create"),
            updatesub = new TicketSubscription(this.user.unique_id, "update"),
            deletesub = new TicketSubscription(this.user.unique_id, "delete");
        createsub.connect();
        updatesub.connect();
        deletesub.connect();
        createsub.subscribe(this.ticketCreated);
        updatesub.subscribe(this.ticketUpdated);
        deletesub.subscribe(this.ticketDeleted);
    },
    beforeDestroy() {
        this.stopCounter();
    }
};
</script>
<style scoped>
.ticketPanel {
    text-align: center;
}
.title {
    font-size: 1.5em;
    line-height: 1.5em;
    margin-bottom: 12px;
    text-transform: inherit;
    letter-spacing: inherit;
    font-family: inherit;
    font-weight: inherit;
}

.content {
    font-size: 1.1em;
}
input.clean {
    width: 100%;
    background: #fafafa;
    padding: 0.5em;
    font-size: 1em;
    border: none;
    border-bottom: 1px solid #c6c6c6;
    margin: 8px auto;
    text-align: center;
}
input.clean:focus {
    outline: none;
}
button.button {
    font-size: 1.1em;
    text-transform: uppercase;
    font-weight: 700;
    padding: 0.7em 1em;
}
#rating {
    margin-top: 12px;
}
#rating .rating {
    margin-bottom: 12px;
}
#rating .comments {
    height: auto;
    min-height: 0;
}
</style>
