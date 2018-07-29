<script>
import { Pie } from "vue-chartjs";
export default {
    props: ["data_points", "options", "labels"],
    extends: Pie,
    watch: {
        data_points(val) {
            this.renderChart(this.data, this.options);
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
        data() {
            return {
                labels: this.labels,
                datasets: [
                    {
                        backgroundColor: this.bgColor,
                        data: this.data_points
                    }
                ]
            };
        }
    },
    mounted() {
        this.renderChart(this.data, this.options);
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
