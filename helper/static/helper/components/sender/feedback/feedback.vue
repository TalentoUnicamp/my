<template>
    <div>
        <div class="title">
            Como foi?
        </div>
        <p>
            Avalie sua experiência com {{ ticket.claimer.full_name }}
        </p>
        <div id="ticketRating" class="ui massive star rating"></div>
        <br>
        <div class="ui form">
            <div class="field">
                <label>Você tem algum comentário? (Opcional)</label>
                <textarea class="comments" rows="2" v-model="comments"></textarea>
            </div>
            <sui-button fluid primary :disabled="!rating" @click="submitFeedback" content="Enviar Feedback"/>
        </div>
    </div>
</template>
<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
export default {
    props: ["ticket", "helper_context"],
    data() {
        return {
            helper: this.helper_context,
            rating: null,
            comments: ""
        };
    },
    methods: {
        submitFeedback() {
            axios
                .patch(this.helper.api.list_tickets + this.ticket.id + "/", {
                    rating: this.rating,
                    comments: this.comments
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        }
    },
    mounted() {
        var comp = this;
        $("#ticketRating").rating({
            onRate: function(rate) {
                comp.rating = rate;
            },
            maxRating: 5
        });
    }
};
</script>
<style scoped>
.title {
    font-size: 1.5em;
    line-height: 1.5em;
    margin-bottom: 12px;
    text-transform: inherit;
    letter-spacing: inherit;
    font-family: inherit;
    font-weight: inherit;
}
.ui.form .field > label {
    font-size: .8em;
    margin-top: .5em;
}
button {
    text-transform: uppercase;
}
</style>
