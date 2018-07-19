<template>
    <div>
        <br>
        <div class="small title">
            Inscrever participantes
        </div>
        <br>
        <sui-form @submit.prevent="submitForm()">
            <sui-container text-align="center">
                <sui-button color="blue" content="Criar participante em branco"
                v-bind:disabled="disableSubmitButton"/>
            </sui-container>
        </sui-form>
        <span v-if="token.length > 0">
            <sui-divider />
            <h2 class="ui header">
                <div class="content">
                    Completar aplicação
                    <div class="sub header">Forneça o token ao participante ou acesse a conta dele(a) para completar a aplicação</div>
                </div>
            </h2>
            <h3 class="ui header">
                <div class="content">
                    Token: <code id="tokenText" class="tokencode" @click="copyToken()">{{ token }}</code>
                    <div v-if="tokenCopied" class="ui left pointing black basic label">
                        Copiado!
                    </div>
                </div>
            </h3>
            <h2 class="ui header">
                <div class="content">
                    <div class="sub header">Se preferir, faça o login diretamente:</div>
                </div>
            </h2>
            <sui-button color="green" @click="loginAs()" content="Fazer login" />
            <br>
            <h2 class="ui header">
                <div class="content">
                    <div class="sub header">Ou clique na URL para copiá-la:</div>
                </div>
            </h2>
            <div class="ui form">
                <div class="field">
                    <a @click="copyURL()"><code id="urlText">{{ loginUrl }}</code></a>
                    <br>
                    <div v-if="urlCopied" class="ui up pointing black basic label">
                        Copiado!
                    </div>
                </div>
            </div>
        </span>
    </div>
</template>

<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";

export default {
    props: ["staff_context"],
    data() {
        return {
            staff: this.staff_context,
            token: "",
            loginUrl: "",
            urlCopied: false,
            tokenCopied: false
        };
    },
    computed: {
        disableSubmitButton() {
            return (
                !this.urlCopied && !this.tokenCopied && this.token.length > 0
            );
        }
    },
    methods: {
        submitForm() {
            this.urlCopied = false;
            this.tokenCopied = false;
            this.token = "";
            self = this;
            axios
                .post(this.staff.api.create_blank_hacker)
                .then(function(data) {
                    (self.token = data.data.token),
                        (self.loginUrl = data.data.url);
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
        },
        loginAs() {
            document.location.href = this.loginUrl;
        },
        copyURL() {
            this.copyTextToClipboard(this.loginUrl);
            this.urlCopied = true;
        },
        copyToken() {
            this.copyTextToClipboard(this.token);
            this.tokenCopied = true;
        },
        copyTextToClipboard(str) {
            let el = document.createElement("textarea");
            el.value = str;
            document.body.appendChild(el);
            el.select();
            document.execCommand("copy");
            document.body.removeChild(el);
        }
    }
};
</script>

<style scoped>
.ui.basic.black.label {
    color: white !important;
    background-color: black !important;
    cursor: pointer;
}
code {
    cursor: pointer;
}
.tokencode {
    color: rgba(0, 0, 255, 0.6);
}
</style>
