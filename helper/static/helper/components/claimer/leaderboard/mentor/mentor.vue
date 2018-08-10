<template>
    <div class="item">
        <div class="content">
            <strong>{{ mentor.profile.full_name }}</strong>
            <p>
                <strong>{{ mentor.rank }}</strong> <i class="ui yellow star icon"></i> ({{ numTickets }} Tickets)
            </p>
        </div>
    </div>
</template>
<script>
export default {
    props: ["mentor"],
    computed: {
        numTickets() {
            return this.mentor.claimed_tickets.filter(
                ticket => ticket.state == "completed"
            ).length;
        }
    }
};
</script>
