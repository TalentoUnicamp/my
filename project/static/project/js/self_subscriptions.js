import { SelfSubscription } from "model_sockets/js/subscription";

var selfsub = new SelfSubscription("update", false);
selfsub.connect();

// function update(data) {
//     console.log(data);
// }

// selfsub.subscribe(update);

export default selfsub;
