<template>
    <div>
        <sui-divider />
        <br>
        <div class="header divided title">
            Lembretes
        </div>
        <p style="text-align: center;">
            Criamos um mini-app pra você não esquecer de levar nada!<br>
            Salvamos seus itens em cookies, então eles não serão sincronizados entre navegadores<br>
            Clique nos itens para apagá-los/marcar como completos
        </p>
        <sui-list>
            <ReminderItem
            v-for="item in cmpItems"
            :item="item"
            :key="item.id"
            @delete="items.splice($event, 1)"/>
        </sui-list>
        <sui-form @submit.prevent="addItem">
            <sui-input v-model="newItem" placeholder="Adicionar item" />
            <sui-button content="Adicionar" icon="plus" @click="addItem" color="blue" />
        </sui-form>
        <br>
    </div>
</template>

<script>
import ReminderItem from "./reminder_item.vue";

export default {
    components: { ReminderItem },
    data() {
        return {
            defaultItems: ["RA/RG", "Celular (muito importante)", "Currículo impresso (vai que pedem)"],
            items: [],
            newItem: ""
        };
    },
    watch: {
        items(val) {
            this.$cookie.set("reminders", JSON.stringify(val), 120);
        }
    },
    computed: {
        cmpItems() {
            var cmp = [];
            for (let item in this.items) {
                cmp.push({ id: item, content: this.items[item] });
            }
            return cmp;
        }
    },
    methods: {
        addItem() {
            if (this.newItem == "") return;
            this.items.push(this.newItem);
            this.newItem = "";
        }
    },
    mounted() {
        var local = this.$cookie.get("reminders");
        if (local === null) {
            local = this.defaultItems;
        } else {
            local = JSON.parse(local);
        }
        this.items = local;
    }
};
</script>
