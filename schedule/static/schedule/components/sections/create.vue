<template>
    <div>
        <br>
        <div>
            <h2 class="ui header centered">
                <div class="content">
                    Criar eventos
                    <div class="sub header">Todos os eventos que você participou estão aqui<br>Não se esqueça de dar seu feedback!</div>
                </div>
            </h2>
        </div>
        <br>
        <sui-form equalWidth @submit.prevent="createEvent" :loading="loadingForm">
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
                    <div class="ui calendar" id="start">
                        <div class="ui input left icon">
                            <i class="calendar icon"></i>
                            <input type="text" placeholder="Início">
                        </div>
                    </div>
                </sui-form-field>
                <sui-form-field>
                    <label>Duração*</label>
                    <div class="ui calendar" id="duration">
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
            <sui-form-fields>
                <sui-form-field>
                    <label>Palestrante</label>
                    <select id="speaker" class="ui search selection dropdown" placeholder="Selecione alguém"></select>
                </sui-form-field>
            </sui-form-fields>
            <sui-button icon="plus" :disabled="!allowCreate" content="Criar evento" color="blue" />
        </sui-form>

        <List
        :schedule_context="schedule" />

    </div>
</template>
<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import moment from "project/js/moment";
import List from "./create/list.vue";

export default {
    props: ["schedule_context"],
    components: { List },
    data() {
        return {
            schedule: this.schedule_context,
            loadingForm: false,
            data: {},
            typeOptions: [],
            userProfiles: []
        };
    },
    computed: {
        allowCreate() {
            return (
                this.data.name &&
                this.data.description &&
                this.data.event_type &&
                this.data.start &&
                this.data.duration &&
                (this.data.require_register ? this.data.max_attendees : true)
            );
        }
    },
    methods: {
        getEventTypeOptions() {
            var comp = this;
            axios
                .options(this.schedule.api.create_event)
                .then(function(data) {
                    comp.typeOptions = data.data.actions.POST.event_type.choices.map(
                        choice => {
                            return {
                                key: choice.value,
                                value: choice.value,
                                text: choice.display_name
                            };
                        }
                    );
                })
                .catch(error => {
                    console.log(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        createEvent() {
            if (!this.data.max_attendees) this.data.max_attendees = 0;
            self = this;
            this.loadingForm = true;
            axios
                .post(this.schedule.api.create_event, this.data)
                .then(data => {
                    self.data = {};
                    $("#start").calendar("clear");
                    $("#duration").calendar("clear");
                    $("#speaker").dropdown("clear");
                    toast("Pronto!", "Evento criado", "success");
                })
                .catch(error => {
                    console.log(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                })
                .then(data => {
                    self.loadingForm = false;
                });
        }
    },
    mounted: function() {
        this.getEventTypeOptions();
        var comp = this;
        $("#start").calendar({
            ampm: false,
            onChange: function(date, text, mode) {
                comp.data["start"] = moment(date).format();
                comp.data = JSON.parse(JSON.stringify(comp.data));
            }
        });
        $("#duration").calendar({
            ampm: false,
            type: "time",
            onChange: function(date, text, mode) {
                comp.data["duration"] = moment(date).format("HH:mm");
                comp.data = JSON.parse(JSON.stringify(comp.data));
            }
        });
        $("#speaker").dropdown({
            apiSettings: {
                url: comp.schedule.api.sui_list_profiles + "?search={query}",
                cache: false
            },
            filterRemoteData: false,
            saveRemoteData: false,
            onChange: function(value) {
                comp.data["speaker_unique_id"] = value;
            }
        });
    }
};
</script>
