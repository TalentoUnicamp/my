<template>
    <div class="container">
        <br>
        <div>
            <h2 class="ui header divided centered">
                <div class="content">
                    Configurações
                    <div class="sub header">Alterações aqui se refletem em quase tudo do app</div>
                </div>
            </h2>
        </div>
        <sui-divider />
        <sui-form @submit.prevent="saveChanges">
            <div class="divided title">Padrões</div>
            <sui-form-fields fields="two">
                <sui-form-field>
                    <sui-checkbox label="Inscritos são staff por padrão" toggle v-model="default_staff"/>
                </sui-form-field>
                <sui-form-field>
                    <sui-checkbox label="Inscritos são hacker por padrão" toggle v-model="default_hacker"/>
                </sui-form-field>
            </sui-form-fields>
            <sui-form-fields fields="two">
                <sui-form-field>
                    <sui-checkbox label="Hackers são admitidos por padrão" toggle v-model="auto_admit"/>
                </sui-form-field>
                <sui-form-field>
                    <sui-checkbox label="Fila do helper aberta" toggle v-model="ticket_queue_open"/>
                </sui-form-field>
            </sui-form-fields>
            <sui-form-fields fields="two">
                <sui-form-field>
                    <sui-checkbox label="Exigir emails válidos" toggle v-model="verify_email"/>
                </sui-form-field>
            </sui-form-fields>
            <sui-form-fields fields="two">
                <sui-form-field>
                    <label>Número máximo de participantes <small style="color: gray;">0 para sem limites</small></label>
                    <sui-input v-model="max_hackers" type='number' placeholder="Máximo de participantes" />
                </sui-form-field>
                <sui-form-field>
                    <label>Minutos para tickets expirarem <small style="color: gray;">0 para não expirarem</small></label>
                    <sui-input v-model="ticket_expire" type='number' placeholder="30" />
                </sui-form-field>
            </sui-form-fields>
            <div class="divided title">Datas</div>
            <sui-form-fields fields="two">
                <sui-form-field>
                    <label>Abertura do registro</label>
                    <div class="ui calendar" id="registration_open">
                        <div class="ui input left icon">
                            <i class="calendar icon"></i>
                            <input type="text" placeholder="Abertura registro">
                        </div>
                    </div>
                </sui-form-field>
                <sui-form-field>
                    <label>Fechamento do registro</label>
                    <div class="ui calendar" id="registration_close">
                        <div class="ui input left icon">
                            <i class="calendar icon"></i>
                            <input type="text" placeholder="Fechamento registro">
                        </div>
                    </div>
                </sui-form-field>
            </sui-form-fields>
            <sui-form-fields fields="three">
                <sui-form-field>
                    <label>Prazo de confirmação</label>
                    <div class="ui calendar" id="confirmation">
                        <div class="ui input left icon">
                            <i class="calendar icon"></i>
                            <input type="text" placeholder="Prazo confirmação">
                        </div>
                    </div>
                </sui-form-field>
                <sui-form-field>
                    <label>Início do evento</label>
                    <div class="ui calendar" id="hackathon_start">
                        <div class="ui input left icon">
                            <i class="calendar icon"></i>
                            <input type="text" placeholder="Início evento">
                        </div>
                    </div>
                </sui-form-field>
                <sui-form-field>
                    <label>Fim do evento</label>
                    <div class="ui calendar" id="hackathon_end">
                        <div class="ui input left icon">
                            <i class="calendar icon"></i>
                            <input type="text" placeholder="Fim evento">
                        </div>
                    </div>
                </sui-form-field>
            </sui-form-fields>
            <sui-button fluid content="Salvar alterações" color="blue" />
        </sui-form>
        <br/>
    </div>
</template>

<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import moment from "project/js/moment";

export default {
    props: ["admin_context", "settings_context"],
    data() {
        return {
            admin: this.admin_context,
            settings: this.settings_context,
            default_staff: this.settings_context["default_staff"],
            default_hacker: this.settings_context["default_hacker"],
            auto_admit: this.settings_context["auto_admit_hackers"],
            max_hackers: this.settings_context["max_hackers"],
            ticket_expire: this.settings_context["ticket_expire"],
            ticket_queue_open: this.settings_context["ticket_queue_open"],
            verify_email: this.settings_context["verify_email"]
        };
    },
    watch: {
        settings: {
            handler(data) {
                this.default_hacker = data["default_hacker"];
                this.default_staff = data["default_staff"];
                this.auto_admit = data["auto_admit_hackers"];
                this.max_hackers = data["max_hackers"];
                this.ticket_expire = data["ticket_expire"];
                this.ticket_queue_open = data["ticket_queue_open"];
                this.verify_email = data["verify_email"];
                this.refreshCalendars(data);
            },
            deep: true
        }
    },
    methods: {
        refreshCalendars(data) {
            for (let key in data) {
                if (key.endsWith("seconds")) {
                    let k = key.replace("_seconds", "");
                    let value = data[key];
                    let date = moment(value).toDate();
                    $("#" + k).calendar("set date", date);
                }
            }
        },
        saveChanges() {
            let data = {
                _default_hacker: this.default_hacker,
                _default_staff: this.default_staff,
                auto_admit: this.auto_admit,
                max_hackers: this.max_hackers,
                ticket_expire: this.ticket_expire,
                ticket_queue_open: this.ticket_queue_open,
                verify_email: this.verify_email,
                registration_open: moment(
                    $("#registration_open").calendar("get date")
                ).format(),
                registration_close: moment(
                    $("#registration_close").calendar("get date")
                ).format(),
                confirmation: moment(
                    $("#confirmation").calendar("get date")
                ).format(),
                hackathon_start: moment(
                    $("#hackathon_start").calendar("get date")
                ).format(),
                hackathon_end: moment(
                    $("#hackathon_end").calendar("get date")
                ).format()
            };
            axios
                .put(this.admin.api.update_settings, data)
                .then(function(data) {
                    toast("Sucesso", "Configurações alteradas", "success");
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        }
    },
    mounted() {
        $("#registration_open").calendar({
            ampm: false,
            endCalendar: $("#registration_close")
        });
        $("#registration_close").calendar({
            ampm: false,
            startCalendar: $("#registration_open")
        });
        $("#hackathon_start").calendar({
            ampm: false,
            endCalendar: $("#hackathon_end")
        });
        $("#hackathon_end").calendar({
            ampm: false,
            startCalendar: $("#hackathon_start")
        });
        $("#confirmation").calendar({
            ampm: false
        });
        this.refreshCalendars(this.settings);
    }
};
</script>
