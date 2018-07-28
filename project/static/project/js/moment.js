import * as mome from 'moment';
import "moment/locale/pt-br";

if ("default" in mome) {
    var moment = mome["default"];
} else {
    var moment = mome;
}

moment.locale("pt-BR");

export default moment;
