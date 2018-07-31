<template>
    <sui-card>
        <sui-card-content>
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
        <sui-button-group attached="bottom" :widths="n_buttons">
            <sui-button v-if="event.require_register" @click="$emit('see-details', event)" color="green">
                <sui-icon name="coffee" /> Detalhes
            </sui-button>
            <sui-button @click="$emit('edit-event', event)" color="blue">
                <sui-icon name="edit" /> Editar
            </sui-button>
        </sui-button-group>
    </sui-card>
</template>
<script>
    import moment from 'project/js/moment'

    export default {
        props: ['event'],
        filters: {
            calendar(date) {
                if (moment().add(7, 'days').isBefore(moment(date))) {
                    return moment(date).format('D [de] MMM [às] HH:mm');
                }
                return moment(date).calendar()
            },
            time(time) {
                return moment(time, "HH:mm:ss").format('HH:mm')
            }
        },
        computed: {
            n_buttons() {
                return this.event.require_register ? 2 : 1;
            }
        }
    }
</script>

<style scoped>
.ui.cards > .card {
    font-size: .9em;
}
.ui.buttons .button, .ui.buttons .or, .ui.button {
    font-size: .8rem;
}
</style>
