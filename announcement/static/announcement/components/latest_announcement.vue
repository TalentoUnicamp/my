<template>
    <div v-if="announcement !== null" class="row">
        <div class="column">
            <Announcement
            v-bind:announcement="announcement"
            v-bind:allowDelete="false" />
        </div>
    </div>
</template>

<script>
    import axios from "project/js/axios_csrf";
    import Announcement from "./announcement.vue";

    import { ModelSubscription } from "model_sockets/js/subscription";

    export default {
        components: { Announcement },
        data() {
            return {
                announcement: null,
                sidebar: sidebar_context
            };
        },
        methods: {
            getLatestAnnouncement(deleted) {
                if (
                    this.announcement !== null &&
                    deleted.id !== this.announcement.id
                    )
                    return;
                var comp = this;
                axios.get(this.sidebar.api.get_announcement).then(function(data) {
                    data = data.data;
                    if (data.length > 0) comp.announcement = data[0];
                    else comp.announcement = null;
                });
            },
            setLatestAnnouncement(announcement) {
                this.announcement = announcement;
            }
        },
        mounted: function() {
            this.getLatestAnnouncement();

            var createsub = new ModelSubscription(
                "announcement",
                "Announcement",
                "create"
                );
            var deletesub = new ModelSubscription(
                "announcement",
                "Announcement",
                "delete"
                );
            createsub.connect();
            deletesub.connect();
            createsub.subscribe(this.setLatestAnnouncement);
            deletesub.subscribe(this.getLatestAnnouncement);
        }
    };
</script>
