<template>
    <div id="admin" class="page">
        <div class="divided title">
            Admin
        </div>
        <div class="ui stackable centered page grid">
            <LatestAnnouncement />
            <div class="row">
                <div class="column">
                    <sui-menu class="stackable five item">
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
                    v-bind:admin_context="admin"
                    v-show="isActive('Listar usuários')" />
                    <Create
                    v-show="isActive('Criar usuários')" />
                    <Company
                    v-bind:admin_context="admin"
                    v-show="isActive('Empresas')" />
                    <Announcements
                    v-bind:admin_context="admin"
                    v-show="isActive('Anúncios')" />
                    <Settings
                    v-bind:admin_context="admin"
                    v-bind:settings_context="settings"
                    v-show="isActive('Configurações')" />

                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import List from "./sections/list.vue";
    import Create from "./sections/create_users.vue";
    import Company from "./sections/company.vue";
    import Settings from "./sections/settings.vue";
    import Announcements from "./sections/announcements.vue";

    import LatestAnnouncement from "announcement/components/latest_announcement.vue";


    export default {
        props: ["admin_context", "settings_context"],
        components: {
            List,
            Create,
            Company,
            Settings,
            Announcements,
            LatestAnnouncement
        },
        data() {
            return {
                admin: this.admin_context,
                settings: this.settings_context,
                active: "Listar usuários",
                items: [
                "Listar usuários",
                "Criar usuários",
                "Empresas",
                "Anúncios",
                "Configurações"
                ]
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
