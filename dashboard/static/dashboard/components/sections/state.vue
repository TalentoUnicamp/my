<template>
    <div>
        <div class="small title">
            Seu Status:
        </div>
        <br>
        <div :class="user.state" class="state">
            {{ stateText }}
        </div>
        <p>
            {{ helperText }}
        </p>
        <br>
    </div>
</template>

<script>
    export default {
        props: ['user_context'],
        data() {
            return {
                user: this.user_context
            }
        },
        computed: {
            stateText() {
                var map = {
                    'unverified': 'Confirmar Email',
                    'incomplete': 'Aplicação incompleta',
                    'late': 'Inscrições Encerradas',
                    'submitted': 'Aplicação Enviada',
                    'declined': 'Aplicação Recusada',
                    'admitted': 'Aplicação Aprovada',
                    'waitlist': 'Fila de Espera',
                    'withdraw': 'Desistência',
                    'confirmed': 'Confirmado',
                    'checkedin': 'Check-in Realizado'
                }
                return map[this.user.state];
            },
            helperText() {
                var map = {
                    'unverified': 'Você precisa verificar seu email.',
                    'incomplete': 'Sua aplicação ainda está incompleta',
                    'late': 'As inscrições encerraram. Quem sabe na próxima!',
                    'submitted': 'Sua aplicação foi enviada e será avalida por nossa equipe :)',
                    'declined': 'Agradecemos por seu interesse no nosso evento, mas infelizmente sua aplicação foi recusada :(',
                    'admitted': 'Sua aplicação foi aceita!',
                    'waitlist': 'Atingimos o máximo de inscritos confirmados e você entrou para a fila de espera',
                    'withdraw': 'Você decidiu se abster dessa edição do nosso evento',
                    'confirmed': 'Tudo está em ordem! Agora é só esperar o dia do evento',
                    'checkedin': ''
                }
                return map[this.user.state];
            }
        }
    }
</script>
