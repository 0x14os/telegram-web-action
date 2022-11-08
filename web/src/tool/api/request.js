import {URL as api} from './api';
import fetch from './service';

let http = {};

http.admin = {

    list: (param) => {
        return fetch({
            url: api.admin.list,
            method: 'get',
            params: param,
        });
    },

    detail: (param) => {
        return fetch({
            url: api.admin.detail,
            method: 'get',
            params: param,
        });
    },

    //软删除
    del: (param) => {
        return fetch({
            url: api.admin.del,
            method: 'get',
            params: param,
        });
    },

    add: (param) => {
        return fetch({
            url: api.admin.add,
            method: 'post',
            data: param,
        });
    },

    editPasswd: (param) => {
        return fetch({
            url: api.admin.editPasswd,
            method: 'post',
            data: param,
        });
    },
    edit: (param) => {
        return fetch({
            url: api.admin.edit,
            method: 'post',
            data: param,
        });
    },

    login: (param) => {
        return fetch({
            url: api.admin.login,
            method: 'post',
            data: param,
        });
    },
    out: (param) => {
        return fetch({
            url: api.admin.out,
            method: 'get',
            params: param,
        });
    },

};

http.memberLogList = (param) => {
    return fetch({
        url: api.account.logList,
        method: 'get',
        params: param,
    });
};


http.group = {
    list: (param) => {
        return fetch({
            url: api.group.list,
            method: 'get',
            params: param,
        });
    }, soAcclist: () => {
        return fetch({
            url: api.group.soAcclist,
            method: 'get',
            params: {},
        });
    },
    start: (param) => {
        return fetch({
            url: api.task.start,
            method: 'get',
            params: param,
        });
    },
    stop: (param) => {
        return fetch({
            url: api.task.stop,
            method: 'get',
            params: param,
        });
    },
};

http.task = {
    list: (param) => {
        return fetch({
            url: api.task.list,
            method: 'get',
            params: param,
        });
    },
    msg: (param) => {
        return fetch({
            url: api.task.msg,
            method: 'get',
            params: param,
        });
    },
    pushEdit: (param) => {
        return fetch({
            url: api.task.pushEdit,
            method: 'post',
            data: param,
        });
    },

    del: (param) => {
        return fetch({
            url: api.task.del,
            method: 'get',
            params: param,
        });
    },

    delMsg: (param) => {
        return fetch({
            url: api.task.delMsg,
            method: 'get',
            params: param,
        });
    },
};


http.load = api.account.load;

http.account = {

    list: (param) => {
        return fetch({
            url: api.account.list,
            method: 'get',
            params: param,
        });
    },

    detail: (param) => {
        return fetch({
            url: api.account.detail,
            method: 'get',
            params: param,
        });
    },

    status: (param) => {
        return fetch({
            url: api.account.status,
            method: 'post',
            data: param,
        });
    },

    joinGroup: (param) => {
        return fetch({
            url: api.account.joinGroup,
            method: 'post',
            data: param,
        });
    },

    edit: (param) => {
        return fetch({
            url: api.account.edit,
            method: 'post',
            data: param,
        });
    },
    load: (param) => {
        return fetch({
            url: api.account.load,
            method: 'post',
            data: param,
        });
    },

    getGroup: (param) => {
        return fetch({
            url: api.account.getGroup,
            method: 'post',
            data: param,
        });
    },


    activation: (param) => {
        return fetch({
            url: api.account.activation,
            method: 'post',
            data: param,
        });
    },

    extract: (param) => {
        return fetch({
            url: api.account.extract,
            method: 'post',
            data: param,
        });
    },

    //群成员列表
    groupUserList: (param) => {
        return fetch({
            url: api.account.groupList,
            method: 'get',
            params: param,
        });
    },

    //所有群成员
    groupUserAll: (param) => {
        return fetch({
            url: api.account.groupUserAll,
            method: 'get',
            params: param,
        });
    },

    //发送验证码
    getCode: (param) => {
        return fetch({
            url: api.account.getCode,
            method: 'post',
            data: param,
        });
    },

    //搜索用户名
    searchUsername: (param) => {
        return fetch({
            url: api.account.searchUsername,
            method: 'post',
            data: param,
        });
    },
    //新建群
    newGroup: (param) => {
        return fetch({
            url: api.account.newGroup,
            method: 'post',
            data: param,
        });
    },
    //发送一条信息到群里
    pushGroupMsg: (param) => {
        return fetch({
            url: api.account.groupPushMsg,
            method: 'post',
            data: param,
        });
    },

    //发送一条信息给某人
    privatePushMsg: (param) => {
        return fetch({
            url: api.account.privatePushMsg,
            method: 'post',
            data: param,
        });
    },

    checkAccount: (param) => {
        return fetch({
            url: api.account.checkAccount,
            method: 'get',
            params: param,
        });
    },
    so: (param) => {
        return fetch({
            url: api.account.so,
            method: 'get',
            params: param,
        });
    },

};

http.msg = {
    list: (param) => {
        return fetch({
            url: api.msg.list,
            method: 'get',
            params: param,
        });
    },count: (param) => {
        return fetch({
            url: api.msg.count,
            method: 'get',
            params: param,
        });
    },read: (param) => {
        return fetch({
            url: api.msg.read,
            method: 'get',
            params: param,
        });
    },
};


http.private = {
    list: (param) => {
        return fetch({
            url: api.private.list,
            method: 'get',
            params: param,
        });
    },
    add: (param) => {
        return fetch({
            url: api.private.add,
            method: 'post',
            data: param,
        });
    },
    edit: (param) => {
        return fetch({
            url: api.private.edit,
            method: 'post',
            data: param,
        });
    },

    del: (param) => {
        return fetch({
            url: api.private.del,
            method: 'get',
            params: param,
        });
    },

    stop: (param) => {
        return fetch({
            url: api.private.stop,
            method: 'get',
            params: param,
        });
    },

    start: (param) => {
        return fetch({
            url: api.private.start,
            method: 'get',
            params: param,
        });
    },
    one: (param) => {
        return fetch({
            url: api.private.one,
            method: 'get',
            params: param,
        });
    },
    logList: (param) => {
        return fetch({
            url: api.private.logList,
            method: 'get',
            params: param,
        });
    },

};


export {http};
