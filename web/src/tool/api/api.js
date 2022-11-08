import {timestamp} from '../fun';


let getUriTimestamp = timestamp();

let accHost = window.location.host ? window.location.host : (self.location.host ? self.location.host : '');
console.log('accHost', accHost);


let Version = '/v1';
let hostUrl = Version;


const URL = {
    login: hostUrl + '/login' + getUriTimestamp,


    task: {
        list: hostUrl + '/task/list'+ getUriTimestamp,
        msg: hostUrl + '/task/list/msg'+ getUriTimestamp,
        pushEdit: hostUrl + '/task/group/edit'+ getUriTimestamp,
        start: hostUrl + '/task/group/start'+ getUriTimestamp,
        stop: hostUrl + '/task/group/stop'+ getUriTimestamp,
        del: hostUrl + '/task/del'+ getUriTimestamp,
        delMsg: hostUrl + '/task/msg/del'+ getUriTimestamp,
    },

    group: {
        list: hostUrl + '/tg/group/list'+ getUriTimestamp,
        soAcclist: hostUrl + '/tg/group/list/so/acc'+ getUriTimestamp,
    },

    admin: {
        detail: hostUrl + '/user/details'+ getUriTimestamp,
        list: hostUrl + '/user/list'+ getUriTimestamp,
        add: hostUrl + '/user/add'+ getUriTimestamp,
        edit: hostUrl + '/user/edit'+ getUriTimestamp,
        editPasswd: hostUrl + '/user/edit/passwd'+ getUriTimestamp,
        del: hostUrl + '/user/del'+ getUriTimestamp,
        login: hostUrl + '/login'+ getUriTimestamp,
        out: hostUrl + '/out' + getUriTimestamp,
    },


    account: {
        detail: hostUrl + '/tg/account/details'+ getUriTimestamp,
        list: hostUrl + '/tg/account/list'+ getUriTimestamp,
        load: hostUrl + '/tg/account/load'+ getUriTimestamp,
        edit: hostUrl + '/tg/account/edit'+ getUriTimestamp,
        status: hostUrl + '/tg/account/status'+ getUriTimestamp,
        getGroup: hostUrl + '/tg/account/get/group'+ getUriTimestamp,
        activation: hostUrl + '/tg/account/activation'+ getUriTimestamp,
        extract: hostUrl + '/tg/account/group/extract'+ getUriTimestamp,
        groupList: hostUrl + '/tg/account/group/user/list'+ getUriTimestamp,
        groupUserAll: hostUrl + '/tg/account/group/user/all'+ getUriTimestamp,
        groupPushMsg: hostUrl + '/tg/account/group/push/msg'+ getUriTimestamp,
        privatePushMsg: hostUrl + '/tg/account/private/push/msg'+ getUriTimestamp,
        getCode: hostUrl + '/tg/account/get/code'+ getUriTimestamp,
        searchUsername: hostUrl + '/tg/account/search/username'+ getUriTimestamp,
        newGroup: hostUrl + '/tg/account/new/group'+ getUriTimestamp,
        joinGroup: hostUrl + '/tg/account/join/group'+ getUriTimestamp,
        checkAccount: hostUrl + '/tg/account/check'+ getUriTimestamp,
        so: hostUrl + '/tg/account/so'+ getUriTimestamp,
    },


    private: {
        list: hostUrl + '/task/private/list'+ getUriTimestamp,
        logList: hostUrl + '/task/private/list/log'+ getUriTimestamp,
        edit: hostUrl + '/task/private/edit'+ getUriTimestamp,
        add: hostUrl + '/task/private/add'+ getUriTimestamp,
        del: hostUrl + '/task/private/del'+ getUriTimestamp,
        stop: hostUrl + '/task/private/stop'+ getUriTimestamp,
        start: hostUrl + '/task/private/start'+ getUriTimestamp,
        one: hostUrl + '/task/private/one'+ getUriTimestamp,
    },



    msg: {
        list: hostUrl + '/msg/list'+ getUriTimestamp,
        count: hostUrl + '/msg/count'+ getUriTimestamp,
        read: hostUrl + '/msg/read'+ getUriTimestamp,
    },




};


export {URL};
