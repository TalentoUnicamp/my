<template>
    <div id="staff" class="page">
        <div class="divided title">
            {{ company.company_name }}
        </div>

        <div class="ui stackable centered page grid">
            <LatestAnnouncement />
            <div class="row">
                <div class="column">
                    <sui-menu class="stackable two item">
                        <a
                        is="sui-menu-item"
                        v-for="item in items"
                        :active="isActive(item)"
                        :key="item"
                        :content="item"
                        @click="select(item)"
                        />
                    </sui-menu>

                    <Scan
                    v-bind:company_context="company"
                    v-show="isActive('Escanear')" />
                    <ScanList
                    v-bind:company_context="company"
                    v-show="isActive('Escaneados')" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Scan from "./sections/scan.vue";
    import ScanList from "./sections/scan_list.vue";
    import LatestAnnouncement from "announcement/components/latest_announcement.vue";

    export default {
        props: ["company_context"],
        components: { Scan, ScanList, LatestAnnouncement },
        data() {
            return {
                company: this.company_context,
                active: "Escanear",
                items: ["Escanear", "Escaneados"]
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
