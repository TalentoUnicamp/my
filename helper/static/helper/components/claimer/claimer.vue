<template>
    <div>
        <br>
        <div class="ui centered stackable two column grid">
            <div class="centered row">
                <div class="nine wide column">
                    <TicketList v-bind:helper_context="helper" v-bind:user_context="user" />
                </div>
                <div class="seven wide column">
                    <Leaderboard v-bind:helper_context="helper" />
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import TicketList from "./list/list.vue";
import Leaderboard from "./leaderboard/leaderboard.vue";

export default {
    props: ["helper_context", "user_context"],
    components: { TicketList, Leaderboard },
    data() {
        return {
            helper: this.helper_context,
            user: this.user_context,
        };
    }
};
</script>
