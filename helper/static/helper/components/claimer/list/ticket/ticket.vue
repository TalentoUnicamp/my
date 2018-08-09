<template>
    <div v-bind:class="{claimed: isClaimed}" class="ui fluid card ticket">
        <div class="content">
            <i class="right floated red remove link cancel button icon"
            v-if="user.is_admin"
            @click="$emit('delete', ticket)" />
            <div class="header">
                {{ ticket.creator.full_name }}
            </div>
            <div class="meta">
                <div class="date">
                    {{ fromNow }}
                </div>
            </div>
            <div class="description">
                {{ ticket.topic }}
                <br>
                ({{ ticket.location }})
            </div>
            <strong> Contato: </strong>
            {{ ticket.contact }}
        </div>
        <div class="extra content">
            <template v-if="isOpen">
                <div v-if="ticket.creator.unique_id == user.unique_id" class="right floated author">
                    Esse é você!
                </div>
                <template v-else>
                    <button class="ui primary fluid push button claim"
                    @click="$emit('claim', ticket)">Pegar ticket</button>
                </template>
            </template>
            <template v-else>
                <template v-if="ticket.claimer.unique_id == user.unique_id">
                    <button class="ui fluid green push button complete"
                    @click="$emit('complete', ticket)">Marcar como completo</button>
                    <button class="ui fluid primary push button reopen"
                    @click="$emit('reopen', ticket)">Reabrir ticket</button>
                </template>
                <div v-else class="right floated author">
                    Pego por {{ ticket.claimer.full_name }}
                </div>
            </template>
        </div>
    </div>
</template>

<script>
    import moment from "project/js/moment";

    export default {
        props: ["ticket", "user_context"],
        data() {
            return {
                user: this.user_context,
                fromNow: null,
                fromNowCounter: null,
                expireEmitter: null
            };
        },
        watch: {
            ticket(val) {
                this.scheduleCounter();
            }
        },
        computed: {
            isOpen() {
                return !this.ticket.claimed;
            },
            isClaimed() {
                return this.ticket.claimed;
            }
        },
        methods: {
            emitExpired() {
                if (!this.isClaimed)
                    this.$emit("expired", this.ticket);
            },
            getMillisecondsToExpire() {
                return Math.abs(moment().diff(moment(this.ticket.expires)));
            },
            clearExpire() {
                if (this.expireEmitter) {
                    clearTimeout(this.expireEmitter);
                    this.expireEmitter = null;
                }
            },
            scheduleExpireEmitter() {
                this.clearExpire();
                this.expireEmitter = setTimeout(() => {
                    this.emitExpired();
                }, this.getMillisecondsToExpire());
            },
            getFromNow() {
                this.fromNow = moment(this.ticket.created).fromNow();
            },
            startCounter() {
                this.fromNowCounter = setInterval(() => {
                    this.getFromNow();
                });
            },
            stopCounter() {
                if (this.fromNowCounter) {
                    clearInterval(this.fromNowCounter);
                    this.fromNowCounter = null;
                    this.fromNow = null;
                }
            },
            scheduleCounter() {
                this.stopCounter();
                this.getFromNow();
                let created_seconds = moment(this.ticket.created).seconds();
                let now_seconds = moment().seconds();
                let diff = created_seconds - now_seconds;
                let sch = diff >= 0 ? diff : 60 + diff;
                setTimeout(() => {
                    this.startCounter();

                }, (sch + 1) * 1000);
            }
        },
        mounted() {
            this.getFromNow();
            this.scheduleCounter();
            this.scheduleExpireEmitter();
        },
        beforeDestroy() {
            this.stopCounter();
            this.clearExpire();
        }
    };
</script>
<style scoped>
.tickets .ticket {
    text-align: left;
    font-size: 1em;
}
button.push {
    font-family: 'Lato', 'Helvetica Neue', 'Helvetica', sans-serif;
    font-weight: 300;
    -webkit-border-radius: 2px;
    -moz-border-radius: 2px;
    -ms-border-radius: 2px;
    border-radius: 2px;
    font-weight: 700;
    color: white;
    display: block;
    position: relative;
    background: none;
    font-size: 1em;
    padding: .7em 1em;
    border: none;
    text-transform: uppercase;
    transition-duration: .2s;
    margin-bottom: .3em;
}
</style>
