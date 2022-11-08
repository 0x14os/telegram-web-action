// 以下文件格式为描述路由的协议格式
// 你可以调整 routerConfig 里的内容
// 变量名 routerConfig 为 iceworks 检测关键字，请不要修改名称

import UserLogin from './pages/UserLogin';
import Dashboard from './pages/Dashboard';

import AdminList from './pages/Admin/List';
import AdminEdit from './pages/Admin/Edit';

import TaskList from './pages/Task/List';
import MsgList from './pages/Task/MsgList';

import AccountList from './pages/Account/List';
import AccountEdit from './pages/Account/Edit';
import AccountEditCode from './pages/Account/EditCode';

import TaskGroup from './pages/Account/TaskGroup';

import EditTask from './pages/Account/EditTask';

import UserList from './pages/Account/UserList';

import UserAll from './pages/Account/UserAll';
import PushMsg from './pages/Account/PushMsg';

import Test from './pages/Test';
import NoticeList from './pages/Notice/List';

import CardList from './pages/CardList';

import PrivateList from './pages/Private/List';
import PrivateListLog from './pages/Private/Log';
import PrivateEdit from './pages/Private/Edit';

import SearchSo from "./pages/Search/So";

const routerConfig = [

    {
        path: '/dashboard',
        component: AccountList,
        auth: true,
    },

    {
        path: '/test',
        component: Test,
        auth: true,
    },
    {
        path: '/notice',
        component: NoticeList,
        auth: true,
    }, {
        path: '/so',
        component: SearchSo,
        auth: true,
    },

    {
        path: '/admin/list',
        component: AdminList,
        auth: true,
    }, {
        path: '/admin/edit/:type/:id',
        component: AdminEdit,
        auth: true,
    },

    {
        path: '/account/list',
        component: AccountList,
        auth: true,
    },
    {
        path: '/account/code/:id',
        component: AccountEditCode,
        auth: true,
    },
    {
        path: '/account/edit/:id',
        component: AccountEdit,
        auth: true,
    },

    {
        path: '/private/list',
        component: PrivateList,
        auth: true,
    },
    {
        path: '/private/log/:id',
        component: PrivateListLog,
        auth: true,
    },
    {
        path: '/private/edit/:id',
        component: PrivateEdit,
        auth: true,
    },

    {
        path: '/account/group/list/:id',
        component: TaskGroup,
        auth: true,
    },

    {
        path: '/account/group/user/:id/:groupId',
        component: UserList,
        auth: true,
    },

    {
        path: '/account/push/msg/:type/:tid/:to/:name/:tgid',
        component: PushMsg,
        auth: true,
    },

    {
        path: '/account/group/all/user',
        component: UserAll,
        auth: true,
    },

    {
        path: '/account/group/task/add',
        component: EditTask,
        auth: true,
    },

    {
        path: '/task/list',
        component: TaskList,
        auth: true,
    },
    {
        path: '/task/msg/list/:id/:title',
        component: MsgList,
        auth: true,
    },


    ////////////////////////////
    {
        path: '/public/login',
        component: UserLogin,
        auth: true,
    },


];

export default routerConfig;
