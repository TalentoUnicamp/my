<script>
import { Bar } from "vue-chartjs";
export default {
    props: ["values", "options", "labels", "title"],
    extends: Bar,
    watch: {
        data_points(val) {
            this.renderChart(
                this.data,
                this.options ? this.options : this.defaultOptions
            );
        }
    },
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
        defaultOptions() {
            return {
                legend: {
                    display: false
                },
                responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: this.title
                }
            };
        },
        data() {
            return {
                labels: this.labels,
                datasets: [
                    {
                        label: this.label,
                        backgroundColor: this.bgColor,
                        data: this.values
                    }
                ]
            };
        }
    },
    mounted() {
        this.renderChart(
            this.data,
            this.options ? this.options : this.defaultOptions
        );
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
