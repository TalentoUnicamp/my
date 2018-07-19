<template>
    <div v-bind:class="{ui: loadingCamera, segment: loadingCamera}">
        <sui-dimmer v-if="loadingCamera" active>
            <sui-loader>Carregando...</sui-loader>
        </sui-dimmer>
        <br>
        <div class="small title">
            Fazer check in
        </div>
        <br>
        <div v-if="error.length > 0" class="ui negative message">
            <div class="header">
                Opa, algo de errado aconteceu!
            </div>
            <p>
                {{ error }}
            </p>
        </div>
        <div v-if="!userAllowed">
            <h2 class="ui header">
                <div class="content">
                    Atenção!
                    <div class="sub header">Leia tudo!</div>
                </div>
            </h2>
            <p>
                O check in funciona usando a câmera do seu dispositivo. Você deve usá-la para escanear os QR codes dos participantes e confirmar o check in assim que verificar que a leitura foi correta.
            </p>
            <p>
                Algumas informações importantes:
            </p>
            <div class="ui bulleted list">
                <div class="item">Apenas o Safari é suportado em dispositivos iOS</div>
                <div class="item">As imagens são processadas em seu dispositivo e não são enviadas ao servidor</div>
            </div>
            <p>
                Ao clicar no botão abaixo, o navegador irá pedir permissão para acessar sua câmera. Você deve <strong>aceitar</strong> para que o app funcione corretamente.
                <br>
                O Chrome só pergunta <strong>uma vez</strong>, então se você negar, terá que manualmente conceder o acesso da câmera ao site.
            </p>
            <sui-button @click="askPermission()" content="Entendi, pode começar!" fluid color="blue" />
            <sui-divider />
            <h3 class="ui header">
                <div class="content">
                    Não quer/pode usar a câmera?
                    <div class="sub header">Basta digitar o ID do usuário abaixo</div>
                </div>
            </h3>
            <sui-form v-on:submit.prevent="onDecode(manualCode)">
                <sui-form-field>
                    <input v-model="manualCode" placeholder="AbCDe123..." >
                </sui-form-field>
                <sui-button primary fluid content="Pesquisa manual" />
            </sui-form>
        </div>
        <div v-if="userAllowed">
            <sui-button color="blue" fluid content="Trocar câmera" @click="toggleCamera" />
            <br>
            <sui-button color="red" fluid content="Parar câmera" @click="stopCamera" />
            <br>
            <sui-divider />
            <qrcode-reader
            @init="onInit"
            @decode="onDecode"
            :video-constraints="constraints"
            :paused="paused"></qrcode-reader>
        </div>
    </div>
</template>

<script>
import axios from "project/js/axios_csrf";
import swal from "sweetalert";
import toast from "project/js/notifications";
import { QrcodeReader } from "vue-qrcode-reader";

export default {
    props: ["staff_context"],
    components: { QrcodeReader },
    data() {
        return {
            staff: this.staff_context,
            loadingCamera: false,
            userAllowed: false,
            paused: false,
            cameraMode: "environment",
            error: "",
            manualCode: ""
        };
    },
    computed: {
        constraints() {
            return {
                facingMode: { ideal: this.cameraMode }
            };
        }
    },
    methods: {
        askPermission() {
            swal({
                title: "Tem certeza?",
                text:
                    "Não esqueça de aceitar quando o navegador pedir permissão!",
                icon: "warning",
                buttons: ["Calma aí", "Entendi e vou aceitar!"]
            }).then(accepted => {
                if (accepted) this.userAllowed = true;
            });
        },
        onDecode(unique_id) {
            this.paused = true;
            this.loadingCamera = true;
            self = this;
            axios
                .post(this.staff.api.fetch_checkin_hacker, {
                    unique_id: unique_id
                })
                .then(function(data) {
                    // API returned some error
                    if (data.data.status == "error") {
                        swal({
                            title: data.data.title,
                            text: data.data.message,
                            icon: "error",
                            buttons: ["Parar", "Tentar de novo"]
                        }).then(keepGoing => {
                            // Ask if user wants to keep going or stop
                            if (keepGoing) {
                                self.reloadCamera();
                            } else {
                                self.stopCamera();
                            }
                        });
                    }
                    // If results are ok
                    else {
                        swal({
                            title: data.data.title,
                            text: data.data.message,
                            icon: "success",
                            buttons: ["Voltar", "Fazer Check-In!"]
                        }).then(fazercheckin => {
                            // If user wants to checkin hacker, call API
                            if (fazercheckin) {
                                axios
                                    .post(self.staff.api.checkin_hacker, {
                                        unique_id: unique_id
                                    })
                                    .then(function(data) {
                                        // If OK, do nothing else
                                    })
                                    .catch(function(error) {
                                        // If error, log
                                        console.error(error);
                                        toast(
                                            "Opa!",
                                            "Algo de errado aconteceu :(",
                                            "error"
                                        );
                                    })
                                    .then(function() {
                                        self.reloadCamera();
                                    });
                            }
                            // If user does not want to checkin, reload camera
                            else {
                                self.reloadCamera();
                            }
                        });
                    }
                })
                .catch(function(error) {
                    // If during the fetch some error occurred
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                    self.reloadCamera();
                });
        },
        reloadCamera() {
            this.paused = false;
            this.loadingCamera = false;
        },
        stopCamera() {
            this.userAllowed = false;
            this.reloadCamera();
        },
        toggleCamera() {
            if (this.cameraMode == "environment") this.cameraMode = "user";
            else this.cameraMode = "environment";
        },
        async onInit(promise) {
            this.loadingCamera = true;
            try {
                await promise;
            } catch (error) {
                if (error.name === "NotAllowedError") {
                    this.error = "Parece que você não deu permissão ao app :(";
                    this.userAllowed = false;
                } else if (error.name === "NotFoundError") {
                    this.error = "Nenhuma câmera encontrada";
                    this.userAllowed = false;
                } else if (error.name === "NotSupportedError") {
                    this.error =
                        "Você não está acessando esse app de um local seguro";
                    this.userAllowed = false;
                } else if (error.name === "NotReadableError") {
                    this.error =
                        "Parece que sua câmera já está sendo usada em outro lugar";
                    this.userAllowed = false;
                } else if (error.name === "OverconstrainedError") {
                    this.error =
                        "Esse erro é minha culpa. Tente novamente ou contate alguém da equipe";
                    this.userAllowed = false;
                } else {
                    this.error =
                        "Seu navegador parece não ter suporte para essa ferramenta";
                    this.userAllowed = false;
                }
            } finally {
                this.loadingCamera = false;
            }
        }
    }
};
</script>
