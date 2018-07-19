<template>
    <sui-list-item
    :icon="icon"
    v-bind:content="item.content"
    @mouseover="icon = 'trash'"
    @mouseleave="icon = 'minus'"
    @click="$emit('delete', item.id)"/>
</template>

<script>
export default {
    props: ["item"],
    data() {
        return {
            icon: "minus"
        };
    }
};
</script>
