import { BaseSubscription } from 'model_sockets/js/subscription';

export default class TicketSubscription extends BaseSubscription {
    constructor(unique_id, signal, debug) {
        super(debug);
        this.unique_id = unique_id;
        this.signal = signal;
        this.url =
            "/ws/subscriptions/tickets/" +
            unique_id +
            "/" +
            signal +
            "/";
    }
}
