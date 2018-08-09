<template>
    <div>
        <div class="feed-title">
            Atualmente na fila:
        </div>
        <div class="ui feed">
            <FeedItem
            v-if="filteredFeed.length > 0"
            v-for="ticket in filteredFeed"
            v-bind:key="ticket.id"
            v-bind:ticket="ticket"
            @expired="ticketDeleted" />
            <template v-else>
                Ninguém na fila!
            </template>
        </div>
    </div>
</template>
<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import moment from "project/js/moment";
import { ModelSubscription } from "model_sockets/js/subscription";
import FeedItem from "./item.vue";

export default {
    props: ["helper_context"],
    components: { FeedItem },
    data() {
        return {
            helper: this.helper_context,
            feed: []
        };
    },
    computed: {
        filteredFeed() {
            return this.feed.filter(
                ticket => ticket.state == 'open' && moment().isBefore(ticket.expires) || ticket.state == 'claimed'
            );
        }
    },
    methods: {
        getFeed() {
            var comp = this;
            axios
                .get(this.helper.api.list_tickets)
                .then(data => {
                    comp.feed = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        ticketUpdated(ticket) {
            let ticketIdx = this.feed.findIndex(obj => obj.id == ticket.id);
            if (ticketIdx >= 0) this.feed.splice(ticketIdx, 1, ticket);
            else {
                this.feed.push(ticket);
                this.feed = this.feed.slice(0);
            }
        },
        ticketDeleted(ticket) {
            let ticketIdx = this.feed.findIndex(obj => obj.id == ticket.id);
            if (ticketIdx >= 0) this.feed.splice(ticketIdx, 1);
        }
    },
    mounted() {
        this.getFeed();
        var createsub2 = new ModelSubscription("helper", "Ticket", "create");
        var updatesub2 = new ModelSubscription("helper", "Ticket", "update");
        var deletesub2 = new ModelSubscription("helper", "Ticket", "delete");
        createsub2.connect();
        updatesub2.connect();
        deletesub2.connect();
        createsub2.subscribe(this.ticketUpdated);
        updatesub2.subscribe(this.ticketUpdated);
        deletesub2.subscribe(this.ticketDeleted);
    }
};
</script>
<style scoped>
.feed-title {
    font-size: 1.2em;
    margin-bottom: 8px;
}
</style>
