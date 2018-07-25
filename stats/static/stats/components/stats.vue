<template>
    <div id="stats" class="page">
        <div class="divided title">
            Stats
        </div>

        <div class="ui stackable centered page grid">
            <div class="row">
                <div class="column">
                    <sui-menu class="stackable four item">
                        <a
                        is="sui-menu-item"
                        v-for="item in items"
                        :active="isActive(item)"
                        :key="item"
                        :content="item"
                        @click="select(item)"
                        />
                    </sui-menu>

                    <HackerStats
                    v-bind:stats_context="stats"
                    v-show="isActive('Participantes')" />

                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import HackerStats from './sections/hacker_stats.vue'

    export default {
        props: ["stats_context", "user_context"],
        components: { HackerStats },
        data() {
            return {
                user: this.user_context,
                stats: this.stats_context,
                active: "Participantes",
                items: ["Participantes", "Aplicações", "Scans", "Tickets"]
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
