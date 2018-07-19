<template>
    <div v-bind:id="'hacker_rate_' + v_idx" style="text-align: center">
        <p>
            Avaliar participantes é opcional, mas te ajudará a lembrar de sua conversa com eles após o evento
        </p>
        <sui-form>
            <sui-form-field>
                <div v-bind:id="'rating_' + v_idx" class="ui heart massive rating edit" data-rating=0 data-max-rating=5></div>
            </sui-form-field>
            <sui-form-field>
                <textarea placeholder="Comentários" @change="$emit('rating_hacker', {rating: rating, comments: comments})" v-model="comments" rows="2" />
            </sui-form-field>
        </sui-form>
    </div>
</template>

<script>
    export default {
        props: ['idx'],
        data() {
            return {
                rating: 0,
                comments: '',
                v_idx: this.idx
            }
        },
        mounted() {
            var comp = this;
            $('#rating_' + this.v_idx).rating({
                clearable: true,
                onInit: true,
                onRate(rate) {
                    comp.rating = rate;
                    comp.$emit('rating_hacker', {rating: comp.rating, comments: comp.comments});
                }
            })
        }
    }
</script>
