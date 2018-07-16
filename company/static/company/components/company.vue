<template>
    <div id="staff" class="page">
        <div class="divided title">
            {{ company.company_name }}
        </div>

        <div class="ui stackable centered page grid">
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

                    <Scan
                    v-bind:company_context="company"
                    v-show="isActive('Escanear')" />
<!--                     <List
                    v-bind:staff_context="staff"
                    v-show="isActive('Lista')" /> -->
<!--


                    <Register
                    v-show="isActive('Inscrição')"
                    v-bind:staff_context="staff" />
 -->
                </div>
        </div>
    </div>
</template>

<script>
    import Scan from './sections/scan.vue';

    export default {
        props: ['company_context'],
        components: { Scan },
        data() {
            return {
                company: this.company_context,
                active: 'Escanear',
                items: ['Escanear', 'Escaneados', 'Inscrição'],
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
