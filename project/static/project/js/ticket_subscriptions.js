import TicketSubscription from "helper/js/ticket_sub.js";

let user = user_context;
let currentTicket = null;

let createsub = new TicketSubscription(user.unique_id, "create"),
    updatesub = new TicketSubscription(user.unique_id, "update"),
    deletesub = new TicketSubscription(user.unique_id, "delete");

export default {
    create: createsub,
    update: updatesub,
    delete: deletesub
};


