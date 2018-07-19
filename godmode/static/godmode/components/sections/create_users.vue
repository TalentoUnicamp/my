<template>
    <div>
        <br>
        <div class="small title">
            Criar usuários
        </div>
        <sui-divider />
        <br>
        <div class="ui two column stackable grid">
            <div class="column">

                <h3 class="ui dividing header">
                    Criar
                </h3>
                <br>
                <sui-form>
                    <sui-form-field>
                        <label>CSV, formato: Primeiro nome, Sobrenome, Email</label>
                        <textarea v-model="csv"></textarea>
                    </sui-form-field>
                </sui-form>
                <br>
                <sui-button color="blue" content="Checar formato" @click="checkFormat()" />

                <sui-button
                v-bind:loading="createLoading"
                v-bind:disabled="createLoading"
                v-if="formatIsValid"
                color="green"
                content="Criar usuários"
                @click="createUsers()" />
                <span v-if="formatIsValid">
                    <br><br>
                </span>
                <sui-checkbox
                v-bind:disabled="createLoading"
                v-if="formatIsValid"
                label="Enviar emails de verificação"
                toggle
                v-model="sendEmails" />

            </div>
            <div class="column">
                <h3 class="ui dividing header">
                    Checar saída
                </h3>
                <div v-if="error.length > 0" class="ui error message">
                    {{ error }}
                </div>
                <div class="ui relaxed list">
                    <div class="item" v-for="user in users" v-bind:key="user.token">
                        <i v-if="user.result == 'success'" class="green large check circle icon"></i>
                        <i v-if="user.result == 'error'" class="red large remove circle icon"></i>
                        <i v-if="user.result == 'pending'" class="large circle outline icon"></i>
                        <div class="content">
                            <div class="header">
                                {{ user.first_name }} {{ user.last_name }}
                            </div>
                            <div class="description">
                                Email:
                                <strong>
                                    {{ user.email }}
                                </strong>

                                <span v-if="user.token.length > 0">
                                     Token:
                                    <strong>
                                        {{ user.token }}
                                    </strong>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";

export default {
    props: ["admin_context"],
    data() {
        return {
            csv: "",
            validCsv: [],
            error: "",
            users: [],
            admin: admin_context,
            createLoading: false,
            sendEmails: false
        };
    },
    computed: {
        formatIsValid() {
            return this.csv.length > 0 && this.csv == this.validCsv;
        }
    },
    methods: {
        checkFormat() {
            this.error = "";
            try {
                this.users = formatCSV(this.csv);
                this.validCsv = this.csv;
            } catch (error) {
                this.error = error;
            }
        },
        createUsers() {
            self = this;
            this.createLoading = true;
            axios
                .post(this.admin.api.batch_create_users, {
                    users: this.users,
                    send_emails: this.sendEmails
                })
                .then(function(data) {
                    self.users = data.data.users;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                })
                .then(function() {
                    self.createLoading = false;
                });
        }
    }
};

function formatCSV(csv) {
    var rows = csv.split("\n");
    if (csv.length == 0) {
        throw "Não tem nada aqui";
    }
    var users = {};
    return rows.map(function(row, i) {
        var columns = row.split(",");
        if (columns.length != 3) {
            throw "Linha " +
                i +
                " tem " +
                columns.length +
                " valores. Eram esperados 3";
        }
        var f_name = columns[0].trim(),
            l_name = columns[1].trim(),
            email = columns[2].trim();
        if (f_name.length == 0 || l_name.length == 0) {
            throw "Linha " + i + ", nome ou sobrenome vazios";
        }
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (!re.test(String(email).toLowerCase())) {
            throw "Linha " + i + ", email inválido";
        }
        if (users[email]) {
            throw "Linha " + i + ", email já digitado";
        }
        users[email] = true;

        return {
            first_name: f_name,
            last_name: l_name,
            email: email,
            result: "pending",
            token: ""
        };
    });
}
</script>
