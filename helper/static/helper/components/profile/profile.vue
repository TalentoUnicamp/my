<template>
    <div class="centered ui stackable page grid">
        <div class="eigth wide column">
            <h1 class="ui title header">Sobre você</h1>
            <div class="ui fluid segment">
                <sui-form @submit.prevent="addSkill">
                    <sui-form-field>
                        <label>Habilidades</label>
                        <div class="ui label" v-for="skill in skills" :key="skill">
                            {{ skill }}
                            <i class="delete skill icon" @click="removeSkill(skill)"></i>
                        </div>
                        <div class="ui fluid action input">
                            <sui-input type="text" v-model="skill" placeholder="Infra, rede, Nodejs, AI, IoT, etc..." />
                            <sui-button color="blue" @click="addSkill" content="Adicionar" />
                        </div>
                    </sui-form-field>
                </sui-form>
                <br>
                <div class="field">
                    <div class="ui fluid green save button" @click="submitProfile">Salvar alterações</div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from "project/js/axios_csrf";
    import toast from "project/js/notifications";
    export default {
        props: ["helper_context"],
        data() {
            return {
                helper: this.helper_context,
                skills: [],
                skill: ""
            }
        },
        methods: {
            submitProfile() {
                axios.patch(this.helper.api.self_mentor, {
                    skills: JSON.stringify(this.skills)
                })
                .then(data => {
                    toast("Pronto!", "Perfil salvo", "success");
                })
                .catch(function(error) {
                    console.error(error);
                    toast("Opa!", "Algo de errado aconteceu :(", "error");
                });
            },
            removeSkill(skill) {
                let skillIdx = this.skills.findIndex(sk => sk === skill);
                this.skills.splice(skillIdx, 1);
            },
            addSkill() {
                if (this.skill.length) {
                    this.skills.push(this.skill.toLowerCase());
                    let s = new Set(this.skills);
                    this.skills = Array.from(s.values());
                    this.skill = '';
                }
            }
        },
        mounted() {
            var comp = this;
            axios
            .get(this.helper.api.self_mentor)
            .then(data => {
                let skills = JSON.parse(data.data.skills);
                if (skills)
                    comp.skills = skills;
                else
                    comp.skills = [];
            })
            .catch(function(error) {
                console.error(error);
                toast("Opa!", "Algo de errado aconteceu :(", "error");
            });
        }
    }
</script>
<style scoped>
.title {
    font-size: 1.5em;
    line-height: 1.5em;
    margin-bottom: 12px;
    text-transform: inherit;
    letter-spacing: inherit;
    font-family: inherit;
    font-weight: inherit;
}
.label {
    margin-bottom: 10px;
}
</style>
