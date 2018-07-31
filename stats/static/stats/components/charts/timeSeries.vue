<script>
import { Line } from "vue-chartjs";
export default {
    props: [
        "data_points",
        "options",
        "title",
        "color",
        "scaleLabel",
        "plotUnit",
        "tickSource"
    ],
    extends: Line,
    watch: {
        data_points(val) {
            this.renderChart(
                this.data,
                this.options ? this.options : this.defaultOptions
            );
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
                        lineTension: 0.3,
                        borderWidth: 2,
                        backgroundColor: this.color
                    }
                ]
            };
        },
        defaultOptions() {
            return {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    xAxes: [
                        {
                            time: {
                                unit: this.plotUnit ? this.plotUnit : "day"
                            },
                            type: "time",
                            distribution: "series",
                            ticks: {
                                source: this.tickSource
                                    ? this.tickSource
                                    : "data"
                            }
                        }
                    ],
                    yAxes: [
                        {
                            scaleLabel: {
                                display: true,
                                labelString: this.scaleLabel
                            }
                        }
                    ]
                }
            };
        }
    }
};
</script>
