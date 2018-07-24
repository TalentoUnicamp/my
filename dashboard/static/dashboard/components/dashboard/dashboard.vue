<template>
    <div id="dashboard" class="page">
        <div class="divided title">
            Dashboard
        </div>
        <div class="ui stackable centered page grid">
            <LatestAnnouncement />
            <div class="row">
                <div class="column">
                    <div class="ui status segment">

                        <!-- Visível a hackers o tempo todo ou para outros não verificados -->
                        <State
                        v-if="user.is_hacker || user.state=='unverified'"
                        v-bind:user_context="user" />

                        <CompleteApp
                        v-if="user.state == 'incomplete'"
                        v-bind:settings_context="settings"
                        v-bind:sidebar_context="sidebar" />

                        <!-- Visível para todos não verificados -->
                        <ResendEmail
                        v-if="user.state=='unverified'"
                        v-bind:user_context="user"
                        v-bind:settings_context="settings"
                        v-bind:dashboard_context="dashboard" />

                        <!-- Visível a hackers que foram admitidos -->
                        <Confirm
                        v-if="user.state=='admitted'"
                        v-bind:user_context="user"
                        v-bind:settings_context="settings"
                        v-bind:dashboard_context="dashboard" />

                        <!-- Visível a hackers que se abstiveram -->
                        <UndoWithdraw
                        v-if="user.state=='withdraw'"
                        v-bind:user_context="user"
                        v-bind:settings_context="settings"
                        v-bind:dashboard_context="dashboard" />

                        <!-- Visível a hackers que confirmaram -->
                        <Info
                        v-if="user.state=='confirmed'"
                        v-bind:settings_context="settings" />

                        <Reminders
                        v-if="user.state=='confirmed'" />

                        <!-- Visível sempre para quem não é hacker ou para hackers confirmados e que fizeram checkin -->
                        <QRid
                        v-if="!user.is_hacker || (user.is_hacker && (user.state=='confirmed' || user.state=='checkedin'))"
                        v-bind:unique_id="user.unique_id" />

                        <!-- Visível a hackers que confirmaram -->
                        <Withdraw
                        v-if="user.state=='confirmed'"
                        v-bind:user_context="user"
                        v-bind:settings_context="settings"
                        v-bind:dashboard_context="dashboard" />

                        <!-- Visível sempre pra todos -->
                        <Access
                        v-bind:dashboard_context="dashboard"
                        v-bind:user_context="user" />

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Access from "dashboard/components/sections/access.vue";
    import QRid from "dashboard/components/sections/qr_id.vue";
    import State from "dashboard/components/sections/state.vue";
    import ResendEmail from "dashboard/components/sections/resend_email.vue";
    import Confirm from "dashboard/components/sections/confirm.vue";
    import UndoWithdraw from "dashboard/components/sections/undo_withdraw.vue";
    import Withdraw from "dashboard/components/sections/withdraw.vue";
    import Info from "dashboard/components/sections/important_info.vue";
    import CompleteApp from "dashboard/components/sections/complete_app.vue";
    import Reminders from "dashboard/components/sections/reminders.vue";

    import LatestAnnouncement from "announcement/components/latest_announcement.vue";

    export default {
        props: [
        "user_context",
        "dashboard_context",
        "settings_context",
        "sidebar_context"
        ],
        components: {
            Access,
            QRid,
            State,
            ResendEmail,
            Confirm,
            UndoWithdraw,
            Withdraw,
            Info,
            CompleteApp,
            Reminders,
            LatestAnnouncement
        },
        data() {
            return {
                user: this.user_context,
                dashboard: this.dashboard_context,
                settings: this.settings_context,
                sidebar: this.sidebar_context
            };
        }
    };
</script>
