import { default as iziToast, IziToastSettings } from 'izitoast';

function toast (title, message, type, timeout = 5000, theme = 'light', position = 'topRight') {
  return iziToast[type](
    {
        title: title,
        message: message,
        type: type,
        timeout: timeout,
        theme: theme,
        position: position
    });
}

export default toast;
