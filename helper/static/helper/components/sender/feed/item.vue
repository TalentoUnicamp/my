<template>
    <div class="event feedTicket">
        <div class="label">
            <i class="circle icon" v-bind:class="{outline: isOpen, claimed: isClaimed}" />
        </div>
        <div class="content">
            <div class="summary">
                {{ ticket.creator.full_name }}
                <div class="date">
                    {{ fromNow }}
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import moment from "project/js/moment";

export default {
    props: ["ticket"],
    data() {
        return {
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
.feed .claimed.icon {
    color: green !important;
    -webkit-animation-name: iconPulse;
    -webkit-animation-duration: 2s;
    -webkit-animation-iteration-count: infinite
}
@-webkit-keyframes iconPulse {
    from {
        opacity: 1
    }

    50% {
        opacity: .5
    }

    to {
        opacity: 1
    }
}
</style>
