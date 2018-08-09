<template>
    <div>
        <br>
        <div class="ui centered stackable two column grid">
            <div class="centered row">
                <div class="column">
                    <TicketPanel
                    :helper_context="helper"
                    :user_context="user"
                    :settings_context="settings"  />
                </div>
                <div class="column">
                    <MentorStats v-bind:helper_context="helper" />
                    <MentorSkills v-bind:helper_context="helper" />
                    <TicketFeed v-bind:helper_context="helper" />
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import TicketPanel from "./ticket_panel/ticket_panel.vue";
import MentorStats from "helper/components/claimer/stats/stats.vue";
import MentorSkills from "helper/components/claimer/skills/skills.vue";
import TicketFeed from "helper/components/sender/feed/feed.vue";

export default {
    props: ["helper_context", "user_context", "settings_context"],
    components: { TicketPanel, MentorStats, MentorSkills, TicketFeed },
    data() {
        return {
            helper: this.helper_context,
            user: this.user_context,
            settings: this.settings_context,
        };
    }
};
</script>
