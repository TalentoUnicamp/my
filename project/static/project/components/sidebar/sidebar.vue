<template>
    <div>
        <div id="sidebar" v-bind:class="{open: showSidebar}">
            <div class="logo item">
                <img v-bind:src="sidebar.event_logo">
            </div>

            <Item
            v-for="item in items"
            v-bind:item="item"
            v-bind:key="item.tab"
            ></Item>

            <div class="note">
                {{ sidebar.event_name }}
            </div>

        </div>
        <div class="tab" @click="toggleSidebar">
            <img v-if="!showSidebar" v-bind:src="sidebar.event_logo" />
            <span class="close" v-if="showSidebar">&#x2715</span>
        </div>
    </div>

</template>

<script>
    import Item from 'project/components/sidebar/item.vue';

    export default {
        components: {Item},
        props: ['sidebar_context', 'user_context'],
        data() {
            return {
                showSidebar: false,
                sidebar: this.sidebar_context,
                user: this.user_context
            }
        },
        computed: {
            items() {
            return [
            {
                title: 'Dashboard',
                active_tab: this.sidebar.active_tab,
                link: this.sidebar.redirect_urls['dashboard'],
                tab: 'dashboard',
                condition: true
            },
            {
                title: 'Admin',
                active_tab: this.sidebar.active_tab,
                link: this.sidebar.redirect_urls['admin'],
                tab: 'admin',
                condition: this.user.is_admin
            },
            {
                title: 'Staff',
                active_tab: this.sidebar.active_tab,
                link: this.sidebar.redirect_urls['staff'],
                tab: 'staff',
                condition: this.user.is_staff
            },
            {
                title: 'Aplicação',
                active_tab: this.sidebar.active_tab,
                link: this.sidebar.redirect_urls['application'],
                tab: 'application',
                condition: this.user.state == 'incomplete' || this.user.state == 'submitted'
            },
            {
                title: 'Empresa',
                active_tab: this.sidebar.active_tab,
                link: this.sidebar.redirect_urls['company'],
                tab: 'company',
                condition: this.user.is_employee
            },
            {
                title: 'Equipe',
                active_tab: this.sidebar.active_tab,
                link: this.sidebar.redirect_urls['team'],
                tab: 'team',
                condition: true
            },
            {
                title: 'Helper',
                active_tab: this.sidebar.active_tab,
                link: this.sidebar.redirect_urls['helper'],
                tab: 'helper',
                condition: true
            },
            {
                title: 'Judge',
                active_tab: this.sidebar.active_tab,
                link: this.sidebar.redirect_urls['judge'],
                tab: 'judge',
                condition: true
            },
            {
                title: 'Logout',
                active_tab: this.sidebar.active_tab,
                link: this.sidebar.redirect_urls['logout'],
                tab: 'logout',
                condition: true
            }
            ]}
        },
        methods: {
            toggleSidebar: function() {
                this.showSidebar = !this.showSidebar;
            }
        }
    }
</script>
