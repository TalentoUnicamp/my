<template>
    <div id="admin" class="page">
        <div class="divided title">
            Admin
        </div>

        <div class="ui stackable centered page grid">
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

                <List
                v-bind:admin_context="admin"
                v-show="isActive('Listar usuários')" />
                <Create
                v-show="isActive('Criar usuários')" />
                <Company
                v-bind:admin_context="admin"
                v-show="isActive('Empresas')" />

            </div>
        </div>
    </div>
</template>

<script>
    import List from './sections/list.vue';
    import Create from './sections/create_users.vue';
    import Company from './sections/company.vue';

    export default {
        props: ['admin_context'],
        components: { List, Create, Company },
        data() {
            return {
                admin: this.admin_context,
                active: 'Listar usuários',
                items: ['Listar usuários', 'Criar usuários', 'Empresas', 'Configurações'],
            };
        },
        methods: {
            isActive(name) {
                return this.active === name;
            },
            select(name) {
                this.active = name;
            },
        },
    }
</script>
