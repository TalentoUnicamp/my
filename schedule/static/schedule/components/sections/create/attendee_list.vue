<template>
    <div>
        <br>
        <div>
            <h2 class="ui header centered">
                <div class="content">
                    Lista de quem atenderá
                </div>
            </h2>
        </div>
        <br>
        <p style="text-align: center;">O botão abaixo permite fazer o download de todos os participantes em todos os eventos</p>
        <div class="ui one column centered grid">
            <div class="four wide column">
                <DownloadButton v-bind:url="schedule.exports.events" />
            </div>
        </div>
        <br>
    </div>
</template>
<script>
    import DownloadButton from "project/components/extra/download_button.vue";
    export default {
        props: ['schedule_context'],
        components: { DownloadButton },
        data() {
            return {
                schedule: this.schedule_context,
            }
        }
    }
</script>
