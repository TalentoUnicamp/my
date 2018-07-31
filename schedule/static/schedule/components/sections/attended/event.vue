<template>
    <sui-card>
        <sui-card-content>
            <div v-if="rating == 0 && comments == ''" class="ui red ribbon label">Dê seu feedback!</div>
            <sui-card-header>{{ event.name }}</sui-card-header>
            <sui-card-meta>{{ event.start | calendar }}
                <span class="small right floated">
                    <sui-icon name="clock" />{{ event.duration | time }}
                </span>
            </sui-card-meta>
            <sui-card-meta>{{ event.event_type }}</sui-card-meta>
            <sui-card-description>
                {{ event.description }}
            </sui-card-description>
        </sui-card-content>
        <sui-card-content v-if="event.speaker" extra>
            <sui-card-meta>
                Apresentado por:<br>
                <b>{{ event.speaker.full_name }}</b><br>
                {{ event.speaker.email }}
            </sui-card-meta>
        </sui-card-content>
        <sui-card-content extra>
            <div class="ui center aligned">
                <div v-bind:id="'rating_' + event.id" class="ui huge heart rating" data-max-rating="5" v-bind:data-rating="rating"></div>
            </div>
            <br>
            <sui-input
            class="fluid"
            placeholder="Digite seu feedback"
            transparent
            v-model="comments" />
        </sui-card-content>
    </sui-card>
</template>
<script>
    import axios from 'project/js/axios_csrf'
    import toast from 'project/js/notifications'
    import moment from "project/js/moment";
    import debounce from "project/js/debounce";

    export default {
        props: ["event"],
        data() {
            return {
                rating:
                this.event.feedbacks.length > 0
                ? this.event.feedbacks[0].rating
                : 0,
                comments:
                this.event.feedbacks.length > 0
                ? this.event.feedbacks[0].comments
                : ""
            };
        },
        filters: {
            calendar(date) {
                if (moment().add(7, 'days').isBefore(moment(date))) {
                    return moment(date).format('D [de] MMM [às] HH:mm');
                }
                return moment(date).calendar()
            },
            time(time) {
                return moment(time, "HH:mm:ss").format("HH:mm");
            }
        },
        watch: {
            comments: debounce(function(val) {
                this.submitFeedback();
            }, 1000)
        },
        methods: {
            handleRate(rate) {
                this.rating = rate;
                this.submitFeedback();
            },
            submitFeedback() {
                this.$emit('submit-feedback', {
                    event_id: this.event.id,
                    rating: this.rating,
                    comments: this.comments
                });
            }
        },
        mounted: function() {
            var comp = this;
            $("#rating_" + this.event.id).rating({
                onRate(value) {
                    comp.handleRate(value);
                }
            });
        }
    };
</script>

<style scoped>
.ui.cards > .card {
    font-size: 0.9em;
}
</style>
