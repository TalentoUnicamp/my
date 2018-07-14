<template>
    <div>
        <br>
        <div class="small title">
            Lista de hackers
        </div>
        <my-vuetable></my-vuetable>
    </div>
</template>

<script>
    import axios from 'project/js/axios_csrf';

    import MyVuetable from './vuetable.vue'

    export default {
        components: { MyVuetable },
        props: ['staff_context'],
        data() {
            return {
                staff: this.staff_context,
                items: ['Todos', 'Confirmados', 'Admitidos'],
                active: 'Todos',
                table: Object
            }
        },
        methods: {
            isActive(name) {
                return this.active === name;
            },
            select(name) {
                this.active = name;
                console.log(this.table);
                console.log(this.table.search('a'));
                if (name == 'Todos')
                    this.table[0].search('').columns().search('').draw();
                else if (name == 'Confirmados')
                    this.table[0].column('state:name').search('confirmed').draw();
                else if (name == 'Admitidos')
                    this.table[0].column('state:name').search('admitted').draw();
            }
        },
        mounted: function () {
            var table = $('#example')
            console.log(table);
            table.DataTable({
                "ajax": {
                    url: staff_context.api.list_hackers,
                    dataSrc: ''
                },
                "columns": [
                { "data": "id" },
                { "data": "name" },
                { "data": "state" }
                ]
            });
            console.log(table);
            console.log(this.table);
            this.table = table;
            console.log(this.table[0]);
        }
    }
</script>
