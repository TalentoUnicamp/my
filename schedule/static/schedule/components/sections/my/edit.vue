<template>
    <div>
        <sui-button color="red" floated="right" icon="delete" content="Apagar" @click="deleteEvent" />
        <sui-button icon="arrow left" content="Voltar" color="blue" @click="$emit('go-back')" />
        <br>
        <br>
        <sui-form equalWidth @submit.prevent="editEvent" :loading="loadingForm">
            <sui-form-fields fields="two">
                <sui-form-field>
                    <label>Nome*</label>
                    <sui-input v-model="data.name" placeholder="Meu evento" />
                </sui-form-field>
                <sui-form-field>
                    <label>Tipo*</label>
                    <sui-dropdown
                    placeholder="Tipo"
                    selection
                    :options="typeOptions"
                    v-model="data.event_type" />
                </sui-form-field>
            </sui-form-fields>
            <sui-form-fields>
                <sui-form-field>
                    <label>Descrição*</label>
                    <sui-input v-model="data.description" placeholder="Um evento sobre eventos" />
                </sui-form-field>
            </sui-form-fields>
            <sui-form-fields fields="two">
                <sui-form-field>
                    <label>Data e hora de início*</label>
                    <div class="ui calendar" id="edit_start">
                        <div class="ui input left icon">
                            <i class="calendar icon"></i>
                            <input type="text" placeholder="Início">
                        </div>
                    </div>
                </sui-form-field>
                <sui-form-field>
                    <label>Duração*</label>
                    <div class="ui calendar" id="edit_duration">
                        <div class="ui input left icon">
                            <i class="calendar icon"></i>
                            <input type="text" placeholder="Duração">
                        </div>
                    </div>
                </sui-form-field>
            </sui-form-fields>
            <sui-form-fields fields="two">
                <sui-form-field>
                    <label>Requer registro</label>
                    <sui-checkbox label="" toggle v-model="data.require_register"/>
                </sui-form-field>
                <sui-form-field v-if="data.require_register">
                    <label>Máximo de participantes</label>
                    <input type="number" v-model="data.max_attendees">
                </sui-form-field>
            </sui-form-fields>
            <sui-button icon="save" fluid :disabled="!allowCreate" content="Salvar alterações" color="blue" />
        </sui-form>
    </div>
</template>
<script>
    import axios from 'project/js/axios_csrf'
    import toast from 'project/js/notifications'
    import swal from "sweetalert";
    import moment from 'project/js/moment'

    export default {
        props: ['schedule_context', 'event'],
        data() {
            return {
                schedule: this.schedule_context,
                loadingForm: false,
                data: this.event,
                typeOptions: [],
            }
        },
        computed: {
            allowCreate() {
                return this.data.name &&
                    this.data.description &&
                    this.data.event_type &&
                    this.data.start &&
                    this.data.duration &&
                    (this.data.require_register ? this.data.max_attendees : true)
            }
        },
        methods: {
            getEventTypeOptions() {
                var comp = this;
                axios.options(this.schedule.api.list_events)
                .then(function (data) {
                    comp.typeOptions = data.data.actions.POST.event_type.choices.map(choice => {
                        return {
                            key: choice.value,
                            value: choice.value,
                            text: choice.display_name
                        }
                    })
                })
                .catch(error => {
                    console.log(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                });
            },
            editEvent() {
                if (!this.data.max_attendees)
                    this.data.max_attendees = 0;
                this.loadingForm = true;
                self = this;
                axios.patch(this.schedule.api.my_update_event + this.data.id + '/', this.data)
                .then(data => {
                    toast('Pronto!', 'Alterações salvas', 'success');
                })
                .catch(error => {
                    console.log(error);
                    toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                })
                .then(data => {
                    self.loadingForm = false;
                })
            },
            deleteEvent() {
                var comp = this;
                swal({
                    title: 'Apagar ' + this.data.name + '?',
                    text: 'Essa ação não pode ser desfeita!',
                    dangerMode: true,
                    icon: "warning",
                    buttons: ["Calma aí", "Apagar"]
                })
                .then(apagar => {
                    if (apagar) {
                        axios.delete(comp.schedule.api.my_delete_event + comp.data.id + '/', comp.data)
                        .then(data => {
                            toast('Atenção', 'Evento apagado', 'info');
                            comp.$emit('go-back');
                        })
                        .catch(error => {
                            console.log(error);
                            toast('Opa!', 'Algo de errado aconteceu :(', 'error');
                        });
                    }
                })
            }
        },
        mounted: function() {
            this.getEventTypeOptions();
            var comp = this;
            $("#edit_start").calendar({
                ampm: false,
                onChange: function(date, text, mode) {
                    comp.data['start'] = moment(date).format();
                    comp.data = JSON.parse(JSON.stringify(comp.data));
                }
            });
            $("#edit_start").calendar('set date', moment(this.data.start).toDate());
            $("#edit_duration").calendar({
                ampm: false,
                type: 'time',
                onChange: function(date, text, mode) {
                    comp.data['duration'] = moment(date).format('HH:mm');
                    comp.data = JSON.parse(JSON.stringify(comp.data));
                }
            });
            $("#edit_duration").calendar('set date', moment(this.data.duration, "HH:mm:ss").toDate());
        }
    }
</script>
