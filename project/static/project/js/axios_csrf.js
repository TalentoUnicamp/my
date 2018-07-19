import axios from "axios";
axios.defaults.headers.common["X-CSRFToken"] = csrf_token;

export default axios;
