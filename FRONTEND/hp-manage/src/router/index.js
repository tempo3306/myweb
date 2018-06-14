import Vue from 'vue';
import Router from 'vue-router';
import store from '@/store/index';
import * as types from '@/store/types';
// 页面刷新时，重新赋值token
try{
    if (window.localStorage.getItem('token')) {
        store.commit(types.LOGIN, window.localStorage.getItem('token'));
        let tem = window.localStorage.getItem('codetable');
        console.log(tem);
        if (tem) {
            let data = {'codetable': JSON.parse(tem)};
            console.log(data);
            store.dispatch("resetadd", data);
        }
    }
}
catch (e) {
    console.log(e);
}

//初始化Router
Vue.use(Router);

const login = r => require.ensure([], () => r(require('@/page/login')), 'login');
const manage = r => require.ensure([], () => r(require('@/page/manage')), 'manage');
const home = r => require.ensure([], () => r(require('@/page/home')), 'home');
const addShop = r => require.ensure([], () => r(require('@/page/addShop')), 'addShop');
const addGoods = r => require.ensure([], () => r(require('@/page/addGoods')), 'addGoods');

const addHander = r => require.ensure([], () => r(require('@/page/addHander')), 'addHander');
const addAuction = r => require.ensure([], () => r(require('@/page/addAuction')), 'addAuction');
const addAction = r => require.ensure([], () => r(require('@/page/addAction')), 'addAction');
const addIdentify_code = r => require.ensure([], () => r(require('@/page/addIdentify_code')), 'addIdentify_code');

const handerList = r => require.ensure([], () => r(require('@/page/handerList')), 'handerList');
const auctionList = r => require.ensure([], () => r(require('@/page/auctionList')), 'auctionList');
const actionList = r => require.ensure([], () => r(require('@/page/actionList')), 'actionList');
const identify_codeList = r => require.ensure([], () => r(require('@/page/identify_codeList')), 'identify_codeList');


const vueEdit = r => require.ensure([], () => r(require('@/page/vueEdit')), 'vueEdit');
const adminSet = r => require.ensure([], () => r(require('@/page/adminSet')), 'adminSet');
const sendMessage = r => require.ensure([], () => r(require('@/page/sendMessage')), 'sendMessage');
const explain = r => require.ensure([], () => r(require('@/page/explain')), 'explain');

const routes = [
    {
        path: '/',
        component: login
    },
    {
        path: '/manage',
        component: manage,
        name: '',
        children: [{  //替换 <router-view>
            path: '',
            component: home,
            meta: [],
        },
            {
                path: '/handerList',
                component: handerList,
                meta: {
                    requireAuth: true,
                    nav: ['数据管理', '查看拍手'],   //面包导航
                },
            }, {
                path: '/auctionList',
                component: auctionList,
                meta: {
                    requireAuth: true,
                    nav: ['数据管理', '查看标书'],
                },
            }, {
                path: '/actionList',
                component: actionList,
                meta: {
                    requireAuth: true,
                    nav: ['数据管理', '查看策略'],
                },
            }, {
                path: '/identify_codeList',
                component: identify_codeList,
                meta: {
                    requireAuth: true,
                    nav: ['数据管理', '查看激活码'],
                },
            }, {
                path: '/addHander',
                component: addHander,
                meta: {
                    requireAuth: true,
                    nav: ['添加数据', '添加拍手']
                },
            }, {
                path: '/addAuction',
                component: addAuction,
                meta: {
                    requireAuth: true,
                    nav: ['添加数据', '添加标书']
                },
            }, {
                path: '/addAction',
                component: addAction,
                meta: {
                    requireAuth: true,
                    nav: ['添加数据', '添加策略']
                },
            }, {
                path: '/addIdentify_code',
                component: addIdentify_code,
                meta: {
                    requireAuth: true,
                    nav: ['添加数据', '添加激活码']
                },
            }, {
                path: '/adminSet',
                component: adminSet,
                meta: ['设置', '管理员设置'],
            }, {
                path: '/sendMessage',
                component: sendMessage,
                meta: ['设置', '发送通知'],
            }, {
                path: '/explain',
                component: explain,
                meta: ['说明', '说明'],
            }]
    }
];


const router = new Router({
    routes
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(r => r.meta.requireAuth)) {
        if (store.state.token) {
            next();
        }
        else {
            next({
                path: '/',
                query: {redirect: to.fullPath}
            });
        }
    }
    else {
        next();
    }
});

// 跨域设置


export default router;
