<template>
    <div id="schedule" class="page">
        <div class="divided title">
            Eventos
        </div>

        <div class="ui stackable centered page grid">
            <div class="row">
                <div class="column">
                    <sui-menu v-bind:class="itemNumber" class="stackable item">
                        <a
                        is="sui-menu-item"
                        v-for="item in items"
                        :active="isActive(item)"
                        :key="item"
                        :content="item"
                        @click="select(item)"
                        />
                    </sui-menu>

                    <AllEvents
                    v-bind:schedule_context="schedule"
                    v-if="isActive('Próximos')" />
                    <RegisteredEvents
                    v-bind:schedule_context="schedule"
                    v-if="isActive('Atenderei')" />
                    <AttendedEvents
                    v-bind:schedule_context="schedule"
                    v-if="isActive('Atendi')" />
                    <CheckIn
                    v-bind:schedule_context="schedule"
                    v-if="isActive('Check-In')" />
                    <Create
                    v-bind:schedule_context="schedule"
                    v-if="user.is_admin"
                    v-show="isActive('Criar')" />
                    <My
                    v-bind:schedule_context="schedule"
                    v-if="isActive('Meus eventos')" />

                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'project/js/axios_csrf'
    import toast from 'project/js/notifications'
    import AllEvents from './sections/all.vue'
    import RegisteredEvents from './sections/registered.vue'
    import AttendedEvents from './sections/attended.vue'
    import CheckIn from './sections/checkin.vue'
    import Create from './sections/create.vue'
    import My from './sections/my.vue'

    export default {
        props: ["schedule_context", "user_context"],
        components: { AllEvents, RegisteredEvents, AttendedEvents, CheckIn, Create, My },
        data() {
            return {
                schedule: this.schedule_context,
                user: this.user_context,
                active: "Próximos",
                hasEvents: false,
            };
        },
        computed: {
            items() {
                var base = ['Próximos', 'Atenderei', 'Atendi'];
                if (this.hasEvents) {
                    base.push('Meus eventos');
                }
                if (this.user.is_staff) {
                    base.push('Check-In');
                }
                if (this.user.is_admin) {
                    base.push('Criar');
                }
                return base;
            },
            itemNumber() {
                var map = {
                    3: 'three',
                    4: 'four',
                    5: 'five',
                    6: 'six'
                }
                return map[this.items.length];
            }
        },
        methods: {
            isActive(name) {
                return this.active === name;
            },
            select(name) {
                this.active = name;
                this.getMyEventsList();
            },
            getMyEventsList(event) {
                let self = this;
                axios.get(this.schedule.api.my_list_events)
                .then(data => {
                    if (data.data.length > 0)
                        self.hasEvents = true;
                    else
                        self.hasEvents = false;
                })
                .catch(error => {
                    console.log(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                })
            }
        },
        mounted: function () {
            this.getMyEventsList();
        }
    };
</script>
