<template>
    <div>
        <sui-divider />
        <br>
        <div class="header divided title">
            Identificação
        </div>
        <div class="description">
            Precisa se identificar? Mostre esse código!
        </div>
        <qr-code class="ui image centered" v-bind:size="size" v-bind:text="unique_id" />
        <br><pre>Ou diga: {{ unique_id }}</pre>
        <br>
    </div>
</template>

<script>
    import VueQRCodeComponent from 'vue-qrcode-component'
    export default {
        props: ['unique_id'],
        components: {'qr-code': VueQRCodeComponent},
        data() {
            return {
                size: 250
            }
        }
    }

</script>
