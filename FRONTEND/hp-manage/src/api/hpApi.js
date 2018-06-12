//引入axios
import axios from 'axios';
import ajax from '@/api-config/axios-api';
import {baseUrl, baseImgPath} from '@/config/env';
import {getToken} from '@/utils/auth';
import router from '@/router/index';
import * as types from '@/store/types';
import store from '@/store/index';
import Qs from 'qs';
//全局设置
// axios.defaults.baseURL = baseUrl;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

let cancel, promiseArr = {};
const CancelToken = axios.CancelToken;


//请求拦截器
axios.interceptors.request.use(config => {
    //发起请求时，取消掉当前正在进行的相同请求
    config.headers.Authorization = `JWT ${store.state.token}`;
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded';  //提交的数据按照 key1=val1&key2=val2 的方式进行编码，key 和 val 都进行了 URL 转码
    // config.headers['X-Requested-With'] = 'XMLHttpRequest';


    if (promiseArr[config.url]) {
        promiseArr[config.url]('操作取消');
        promiseArr[config.url] = cancel;
    } else {
        promiseArr[config.url] = cancel;
    }
    return config;
}, error => {
    return Promise.reject(error);
});




//
// axios.interceptors.response.use(response => {
//     return response;
// }, error => {
//
//     console.log(error.config);
//     // 401 清除token信息并跳转到登录页面
//     store.commit(types.LOGOUT);
//     // 只有在当前路由不是登录页面才跳转
//     router.currentRoute.path !== '/' &&
//     router.replace({
//         path: '/',
//         query: {redirect: router.currentRoute.path},
//     });
//     if (error && error.response) {
//         switch (error.response.status) {
//             case 400:
//                 error.message = '错误请求';
//                 break;
//             case 401:
//                 // 401 清除token信息并跳转到登录页面
//                 store.commit(types.LOGOUT);
//                 // 只有在当前路由不是登录页面才跳转
//                 router.currentRoute.path !== '/' &&
//                 router.replace({
//                     path: '/',
//                     query: {redirect: router.currentRoute.path},
//                 });
//                 break;
//             case 403:
//                 error.message = '拒绝访问';
//                 break;
//             case 404:
//                 error.message = '请求错误,未找到该资源';
//                 break;
//             case 405:
//                 error.message = '请求方法未允许';
//                 break;
//             case 408:
//                 error.message = '请求超时';
//                 break;
//             case 500:
//                 error.message = '服务器端出错';
//                 store.commit(types.LOGOUT);
//                 // 只有在当前路由不是登录页面才跳转
//                 router.currentRoute.path !== '/' &&
//                 router.replace({
//                     path: '/',
//                     query: {redirect: router.currentRoute.path},
//                 });
//                 break;
//             case 501:
//                 error.message = '网络未实现';
//                 break;
//             case 502:
//                 error.message = '网络错误';
//                 break;
//             case 503:
//                 error.message = '服务不可用';
//                 break;
//             case 504:
//                 error.message = '网络超时';
//                 break;
//             case 505:
//                 error.message = 'http版本不支持该请求';
//                 break;
//             default:
//                 error.message = `连接错误${error.response.status}`;
//         }
//     } else {
//         error.message = '连接到服务器失败';
//     }
//     // message.error(error);
//     return Promise.reject(error.response);
// });


// http response 拦截器
axios.interceptors.response.use((response) => {
    console.log(response);
    return response;
}, (error) => {
    console.log(error.status);
    return Promise.resolve(error.response);
});

// axios.interceptors.response.use(
//     response => {
//         return response
//     },
//     error => {
//         if (error.response) {
//             switch (error.response.status) {
//                 case 401:
//                     // 401 清除token信息并跳转到登录页面
//                     store.commit(types.LOGOUT);
//
//                     // 只有在当前路由不是登录页面才跳转
//                     router.currentRoute.path !== '/' &&
//                     router.replace({
//                         path: '/',
//                         query: { redirect: router.currentRoute.path },
//                     });
//                 case 500:
//                     // 401 清除token信息并跳转到登录页面
//                     store.commit(types.LOGOUT);
//
//                     // 只有在当前路由不是登录页面才跳转
//                     router.currentRoute.path !== '/' &&
//                     router.replace({
//                         path: '/',
//                         query: { redirect: router.currentRoute.path },
//                     })
//
//             }
//         }
//         // console.log(JSON.stringify(error));//console : Error: Request failed with status code 402
//         return Promise.reject(error.response.data)
//     },
// )
export default {
    //get请求
    get(url, param) {
        return new Promise((resolve, reject) => {
            let AUTHTOKEN = store.state.token;
            axios({
                method: 'get',
                url: baseUrl + url,
                params: param,
                // headers: {'Authorization': AUTHTOKEN},
                cancelToken: new CancelToken(c => {
                    cancel = c;
                })
            }).then(res => {
                resolve(res);
            });
        });
    },
    //post请求
    post(url, param) {
        return new Promise((resolve, reject) => {
            axios({
                method: 'post',
                url: baseUrl + url,
                data: Qs.stringify(param),
                cancelToken: new CancelToken(c => {
                    cancel = c;
                })
            }).then(res => {
                resolve(res);
            });
        });
    }
};
