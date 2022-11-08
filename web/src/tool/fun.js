import {Message} from '@alifd/next';

let msg = {

    show: (text) => {
        Message.show({
            type: 'notice',
            content: text,
            afterClose: () => console.log('Closed the ok'),
        });
    },

    hide: () => {
        Message.hide();
    },
    success: (text) => {
        Message.success(text);
    },
    error: (text) => {
        Message.error(text);
    },
    notice: (text) => {
        Message.notice(text);
    },
    help: (text) => {
        Message.help(text);
    },
    loading: (text) => {
        Message.loading(text);
    },
};


function jump(uri) {
    return window.location.href = uri;
}


/**
 *
 * @returns {{}}
 */
function getDate() {

    var obj = new Date();
    var _this = {};
    //获取当前日期
    _this.date = function () {
        return obj.toLocaleDateString();
    };

    //获取当前时间
    _this.time = function () {
        return obj.toLocaleTimeString();
    };
    return _this;
}


/**
 * 返回时间戳URL参数
 * @returns {string}
 */
function timestamp() {
    let timestamp = Math.round(new Date() / 1000);
    return '?timestamp=' + timestamp;
}


function toTime(time) {
    var timestamp = Date.parse(new Date(time));
    timestamp = timestamp / 1000;
    return timestamp;
}


/**
 * 时间戳转
 * @param timeStamp
 * @returns {string}
 */
function toDate(date, type = 1) {
    return setDate(date, type);
}

function setDate(timeStamp, type = 1) {
    var date = new Date();
    if (type == 1) {
        date.setTime(timeStamp * 1000);
    }
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    m = m < 10 ? ('0' + m) : m;
    var d = date.getDate();
    d = d < 10 ? ('0' + d) : d;
    var h = date.getHours();
    h = h < 10 ? ('0' + h) : h;
    var minute = date.getMinutes();
    var second = date.getSeconds();
    minute = minute < 10 ? ('0' + minute) : minute;
    second = second < 10 ? ('0' + second) : second;
    return y + '-' + m + '-' + d + ' ' + h + ':' + minute + ':' + second;
}


const lo = () => {
    var _this = {};

    _this.add = function (name, val) {
        return localStorage.setItem(name, val);
    };

    _this.get = function (name) {
        return localStorage.getItem(name);
    };

    _this.del = function (name) {
        return localStorage.removeItem(name);
    };

    _this.clear = function () {
        return localStorage.clear();
    };
    return _this;
};


const accessToken = () => {
    const los = lo();
    let token = los.get('token');
    if (token) {
        return token;
    }
    return false;
};


const statusToken = () => {
    const acc = accessToken();
    if (acc) {
        return true;
    } else {
        return false;
    }
};

const logout = () => {
    const los = lo();
    los.clear();
    return true;
};


const isNull = (val) => {
    let iType = typeof (val);
    // console.log("itype:", iType);
    if (iType == "undefined" || val == "0" || val == "null" || val == null || val == '' || val == undefined || val == 0) {
        return true;
    }
    return false;
};


export {timestamp, getDate, setDate, msg, jump, toTime, toDate, statusToken, lo, isNull, accessToken, logout};
