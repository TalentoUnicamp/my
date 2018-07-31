<template>
    <div id="stats" class="page">
        <div class="divided title">
            Stats
        </div>

        <div class="ui stackable centered page grid">
            <div class="row">
                <div class="column">
                    <sui-menu :class="nTabs" class="stackable item">
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
                    v-if="isActive('Participantes')" />
                    <ApplicationStats
                    v-bind:stats_context="stats"
                    v-if="isActive('Aplicações')" />
                    <RawData
                    v-bind:stats_context="stats"
                    v-if="permissionToRawData"
                    v-show="isActive('Dados brutos')" />

                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import HackerStats from './sections/hacker_stats.vue'
    import ApplicationStats from './sections/application_stats.vue'
    import RawData from './sections/raw_data.vue'

    export default {
        props: ["stats_context", "user_context"],
        components: { RawData, HackerStats, ApplicationStats },
        data() {
            return {
                user: this.user_context,
                stats: this.stats_context,
                active: "Participantes",
            };
        },
        methods: {
            isActive(name) {
                return this.active === name;
            },
            select(name) {
                this.active = name;
            }
        },
        computed: {
            permissionToRawData() {
                if (this.user.is_admin) {
                    return true;
                }
                if (this.user.employee_company_access >= 0) {
                    return true;
                }
                return false;
            },
            nTabs() {
                if (this.permissionToRawData)
                    return "three";
                return "two";
            },
            items() {
                let items = ['Participantes', 'Aplicações'];
                if (this.permissionToRawData)
                    items.push('Dados brutos');
                return items;
            }
        }
    };
</script>
