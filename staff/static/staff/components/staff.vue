<template>
    <div id="staff" class="page">
        <div class="divided title">
            Staff
        </div>

        <div class="ui stackable centered page grid">
            <LatestAnnouncement />
            <div class="row">
                <div class="column">
                    <sui-menu class="stackable three item">
                        <a
                        is="sui-menu-item"
                        v-for="item in items"
                        :active="isActive(item)"
                        :key="item"
                        :content="item"
                        @click="select(item)"
                        />
                    </sui-menu>

                    <List
                    v-bind:staff_context="staff"
                    v-show="isActive('Lista')" />

                    <Checkin
                    v-bind:staff_context="staff"
                    v-show="isActive('Check in')" />

                    <Register
                    v-show="isActive('Inscrição')"
                    v-bind:staff_context="staff" />

                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import List from "./sections/list.vue";
    import Checkin from "./sections/checkin.vue";
    import Register from "./sections/register.vue";

    import LatestAnnouncement from "announcement/components/latest_announcement.vue";

    export default {
        props: ["staff_context"],
        components: { List, Checkin, Register, LatestAnnouncement },
        data() {
            return {
                staff: this.staff_context,
                active: "Lista",
                items: ["Lista", "Check in", "Inscrição"]
            };
        },
        methods: {
            isActive(name) {
                return this.active === name;
            },
            select(name) {
                this.active = name;
            }
        }
    };
</script>
