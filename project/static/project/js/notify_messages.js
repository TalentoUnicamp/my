import toast from "./notifications";

for (var i in messages) {
    var message = messages[i];
    toast("", message.message, message.level);
}
