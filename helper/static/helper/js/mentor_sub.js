import { BaseSubscription } from 'model_sockets/js/subscription';

export default class MentorSubscription extends BaseSubscription {
    constructor(debug) {
        super(debug);
        this.url =
            "/ws/subscriptions/online_mentor/";
    }
}
