import { ModelSubscription } from "model_sockets/js/subscription";

var settingssub = new ModelSubscription(
    "settings",
    "Settings",
    "update",
    false
);
settingssub.connect();

// function update(data) {
//     console.log(data);
// }

// selfsub.subscribe(update);

export default settingssub;
