<template>
    <sui-segment basic>
        <sui-dimmer :active="loading" inverted>
            <sui-loader content="Carregando..." />
        </sui-dimmer>
        <vue-plotly :data="data" :layout="layout" :options="{displaylogo: false}" :autoResize="true" />
    </sui-segment>
</template>

<script>
import VuePlotly from "stats/components/vue_plotly.vue";
export default {
    components: { VuePlotly },
    props: ["labels", "values", "title"],
    computed: {
        layout() {
            return {
                title: this.title,
                showLegend: false
            };
        },
        data() {
            return [
                {
                    x: this.labels,
                    y: this.values,
                    type: "scatter",
                    mode: "lines",
                    fill: "tozeroy",
                    name: this.title,
                    line: { shape: "spline", smoothing: 1 }
                }
            ];
        },
        loading() {
            return !this.values || !this.labels || this.values[0] === undefined;
        }
    }
};
</script>
