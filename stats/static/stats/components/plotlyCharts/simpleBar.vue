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
            bgColor() {
                return this.shuffle([
                    "green",
                    "blue",
                    "purple",
                    "orange",
                    "cyan",
                    "red",
                    "yellow",
                    "pink",
                    "#00AF64",
                    "#FFC700"
                    ]).slice(0, this.labels.length);
            },
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
                    type: "bar",
                    marker: {
                        color: this.bgColor
                    }
                }
                ];
            },
            loading() {
                return !this.values || !this.labels || this.values[0] === undefined;
            }
        },
        methods: {
            shuffle(array) {
            // Fisher-Yates shuffle alg
            var currentIndex = array.length,
            temporaryValue,
            randomIndex;
            // Use labels to seed the random func, so same
            // labels yield the same colors
            Math.seedrandom(this.labels);
            // While there remain elements to shuffle...
            while (0 !== currentIndex) {
                // Pick a remaining element...
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex -= 1;

                // And swap it with the current element.
                temporaryValue = array[currentIndex];
                array[currentIndex] = array[randomIndex];
                array[randomIndex] = temporaryValue;
            }

            return array;
        }
    }
};
</script>
