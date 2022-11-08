// 菜单配置
// headerMenuConfig：头部导航配置
// asideMenuConfig：侧边导航配置

const headerMenuConfig = [
  {
    name: '反馈',
    path: '#',
    external: true,
    newWindow: true,
    icon: 'atm',
  },
  {
    name: '帮助',
    path: '#',
    external: true,
    newWindow: true,
    icon: 'help',
  },
];

const asideMenuConfig = [

  {
    name: '账号',
    path: '/dashboard',
    icon: 'clock',
  },
  {
    name: '群组',
    path: '/account/group/list/0',
    icon: 'clock',
  },
  {
    name: '私信',
    path: '/private/list',
    icon: 'clock',
  },
  {
    name: '群成员',
    path: '/account/group/all/user',
    icon: 'smile',
  },
  {
    name: '任务',
    path: '/task/list',
    icon: 'calendar',
  },
  {
    name: '用户',
    path: '/admin/list',
    icon: 'atm',
  },
];

export { headerMenuConfig, asideMenuConfig };
