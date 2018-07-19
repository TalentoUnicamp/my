<template>
    <div>
        <br>
        <div>
            <h2 class="ui header centered">
                <div class="content">
                    Participantes escaneados
                    <div class="sub header">Edite a lista ou faça o download de todos os dados dos participantes em CSV</div>
                </div>
            </h2>
        </div>
        <br>
        <div class="ui form">
            <div class="fields">
                <div class="twelve wide field">
                    <div class="ui left icon fluid input">
                        <i class="search icon"></i>
                        <input type="text" class="searchText" placeholder="Pesquisar por nome ou email" v-model="searchText">
                    </div>
                </div>
                <div class="four wide field">
                    <DownloadButton v-bind:url="company.exports.scanned_hackers" />
                </div>
            </div>
        </div>
        <table class="ui striped sortable table tablet stackable structured">
            <thead>
                <tr>
                    <th colspan="3">Participante</th>
                    <th colspan="2">Quem escaneou</th>
                </tr>
                <tr>
                    <th class="sorted descending">Avaliação</th>
                    <th>Nome</th>
                    <th>Email</th>
                    <th>Nome</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-bind:key="scan.id" v-for="scan in filteredScans">
                    <td v-bind:data-sort-value="scan.rating">
                        <div class="ui heart rating view" v-bind:data-rating="scan.rating" data-max-rating=5></div>
                    </td>
                    <td>
                        <strong>
                            {{ scan.scannee_full_name }}
                        </strong>
                    </td>
                    <td>
                        {{ scan.scannee_email }}
                    </td>
                    <td>
                        <strong>
                            {{ scan.scanner_full_name }}
                        </strong>
                    </td>
                    <td class="right aligned collapsing">
                        <sui-button v-if="scan.comments.length > 0" class="actionbuttons" icon="comment" color="blue" @click="showComment(scan.scannee_full_name, scan.comments)"></sui-button>

                        <sui-button class="actionbuttons" icon="times" color="red" @click="deleteScan(scan.id)"></sui-button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import axios from "project/js/axios_csrf";
    import swal from "sweetalert";
    import toast from "project/js/notifications";
    import { ModelSubscription } from "model_sockets/js/subscription";

    import DownloadButton from 'project/components/extra/download_button.vue'

    export default {
        props: ["company_context"],
        components: { DownloadButton },
        data() {
            return {
                company: this.company_context,
                scanList: [],
                searchText: ""
            };
        },
        computed: {
            filteredScans() {
                return this.scanList.filter(scan => {
                    let neename =
                    scan.scannee_full_name
                    .toLowerCase()
                    .indexOf(this.searchText.toLowerCase()) > -1;
                    let neeemail =
                    scan.scannee_email
                    .toLowerCase()
                    .indexOf(this.searchText.toLowerCase()) > -1;
                    let nername =
                    scan.scanner_full_name
                    .toLowerCase()
                    .indexOf(this.searchText.toLowerCase()) > -1;
                    return neename || neeemail || nername;
                });
            }
        },
        methods: {
            getScanList() {
                var comp = this;
                axios
                .get(this.company.api.scan_list)
                .then(function(data) {
                    comp.scanList = data.data;
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
            },
            scanUpdated(scan) {
                let scanIdx = this.scanList.findIndex(obj => obj.id == scan.id);
                this.scanList.splice(scanIdx, 1, scan);
                this.$up;
            },
            scanCreated(scan) {
                this.scanList.push(scan);
                this.$up;
            },
            scanDeleted(scan) {
                let scanIdx = this.scanList.findIndex(obj => obj.id == scan.id);
                this.scanList.splice(scanIdx, 1);
            },
            deleteScan(id) {
                var comp = this;
                swal({
                    title: "Tem certeza?",
                    text:
                    "Você terá que escanear esse participante manualmente se quiser adicioná-lo de novo!",
                    icon: "warning",
                    buttons: ["Cancelar", "Apagar"],
                    dangerMode: true
                }).then(willDelete => {
                    if (willDelete) {
                        axios
                        .delete(comp.company.api.scan_destroy + id)
                        .then(function(data) {
                            toast("Aviso", "Scan removido", "info");
                        })
                        .catch(function(error) {
                            console.error(error);
                            toast(
                                "Opa!",
                                "Algo de errado aconteceu :(",
                                "error"
                                );
                        });
                    }
                });
            },
            showComment(name, comment) {
                swal({
                    title: name,
                    text: comment,
                    button: "Fechar"
                });
            }
        },
        mounted() {
            this.getScanList();

            var updatesub = new ModelSubscription(
                "company",
                "Scan",
                "update",
                false
                );
            var createsub = new ModelSubscription(
                "company",
                "Scan",
                "create",
                false
                );
            var deletesub = new ModelSubscription(
                "company",
                "Scan",
                "delete",
                false
                );
            updatesub.connect();
            createsub.connect();
            deletesub.connect();
            updatesub.subscribe(this.scanUpdated);
            createsub.subscribe(this.scanCreated);
            deletesub.subscribe(this.scanDeleted);
        },
        updated() {
            $(".rating.view").rating();
            $(".rating.view").rating("disable");
            $(".table").tablesort();
        }
    };
</script>

<style scoped>
.dropdown,
.ui.form .fields .field .ui.input input,
.ui.form .field .ui.input input {
    margin-top: 10px;
}
.ui.button {
    border-radius: 0.28571429rem;
}
.actionbuttons {
    margin-top: 5px;
    margin-bottom: 5px;
}
.ui.icon.input > i.icon:not(.link) {
    margin-top: 7px;
}
.ui.table {
    font-size: 0.8em;
}
</style>
