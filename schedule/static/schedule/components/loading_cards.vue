<template>
    <sui-card-group :items-per-row="3" stackable>
        <sui-card v-for="card in data" v-bind:key="card">
            <sui-card-content>
                <sui-dimmer active inverted>
                    <sui-loader/>
                </sui-dimmer>
                <img class="ui wireframe image" src="https://semantic-ui.com/images/wireframe/paragraph.png">
            </sui-card-content>
        </sui-card>
    </sui-card-group>
</template>

<script>
    export default {
        props: ['loading', 'number'],
        data() {
            return {
                n: this.number ? this.number : 3
            }
        },
        computed: {
            data() {
                var data = [];
                for (let i = 0; i < this.n; i++)
                    data.push(i);
                return data;
            }
        }
    }
</script>
