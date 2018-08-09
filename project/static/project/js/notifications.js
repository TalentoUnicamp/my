import { default as iziToast, IziToastSettings } from "izitoast";

function desktopNotify(message) {
    let title = sidebar_context.event_name;
    let icon = sidebar_context.event_logo_png;
    if (Notification.permission == "granted") {
        var notification = new Notification(title, {
            icon: icon,
            body: message
        });
        notification.onclick = function () {
            window.focus();
        };
    }
}

function toast(
    title,
    message,
    type,
    timeout = 5000,
    theme = "light",
    position = "topRight"
) {
    if (document.hidden) {
        desktopNotify(message);
    }
    return iziToast[type]({
        title: title,
        message: message,
        type: type,
        timeout: timeout,
        theme: theme,
        position: position
    });
}

export default toast;
