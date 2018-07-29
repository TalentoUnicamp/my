<script>
import { Line } from "vue-chartjs";
export default {
    props: ["data_points", "options", "title", "color"],
    extends: Line,
    watch: {
        data_points(val) {
            this.renderChart(this.data, this.options);
        }
    },
    computed: {
        data() {
            return {
                datasets: [
                    {
                        label: this.title,
                        data: this.data_points,
                        type: "line",
                        pointRadius: 1,
                        fill: true,
                        lineTension: .3,
                        borderWidth: 2,
                        backgroundColor: this.color,
                    }
                ]
            };
        }
    }
}
</script>
