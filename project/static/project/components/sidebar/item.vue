<template>
    <div @click="redirect" v-bind:class="{active: isActive}" v-if="item.condition" class="item">
        {{ item.title }}
    </div>
</template>

<script>
export default {
    props: ["item"],
    computed: {
        isActive: function() {
            // active_tab is provided by project/root.html
            return this.item.tab == this.item.active_tab;
        }
    },
    methods: {
        redirect: function() {
            document.location.href = this.item.link;
        }
    }
};
</script>
