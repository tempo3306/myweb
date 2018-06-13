import axios from 'axios';
import qs from 'qs';
import NProgress from 'nprogress';
import {baseUrl} from '@/config/env';
import router from '@/router/index';
import * as types from '@/store/types';
import store from '@/store/index';
import {getToken} from '@/utils/auth';

let cancel, promiseArr = {};
const CancelToken = axios.CancelToken;


//请求拦截器
axios.interceptors.request.use(config => {
    //发起请求时，取消掉当前正在进行的相同请求
    config.headers.Authorization = `JWT ${store.state.token}`;
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded';  //提交的数据按照 key1=val1&key2=val2 的方式进行编码，key 和 val 都进行了 URL 转码
    config.headers['X-Requested-With'] = 'XMLHttpRequest';
    // let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
    // config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
    let csrftoken = getToken();
    console.log("fff", csrftoken);
    config.headers['X-CSRFToken'] =  csrftoken;

    NProgress.start();

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


axios.interceptors.response.use(response => response, error => Promise.resolve(error.response));

function checkStatus(response) {
    NProgress.done();
    if (response.status === 200 || response.status === 304) {
        return response;
    }
    return {
        data: {
            code: response.status,
            message: response.statusText,
            data: response.statusText,
        }
    };
}

function checkCode(res) {
    let code = res.data.code;
    if (code >= 400) {
        switch (code) {
            case 500:
                store.commit(types.LOGOUT);
                // 只有在当前路由不是登录页面才跳转
                router.currentRoute.path !== '/' &&
                router.replace({
                    path: '/',
                    query: {redirect: router.currentRoute.path},
                });
                break;
            case 401:
                // 401 清除token信息并跳转到登录页面
                store.commit(types.LOGOUT);
                // 只有在当前路由不是登录页面才跳转
                router.currentRoute.path !== '/' &&
                router.replace({
                    path: '/',
                    query: {redirect: router.currentRoute.path},
                });
                break;
            case 400:
                //400 代表token过期
                console.log("token 无效");
                break;
            default:
                console.log("NET ERROR");
        }
        }
        return res;
    }

    export default {
        post(url, data) {
            return axios({
                method: 'post',
                url: baseUrl + url,
                data: qs.stringify(data),
                timeout: 30000,
            }).then(checkStatus).then(checkCode);
        },
        get(url, params) {
            return axios({
                method: 'get',
                url: baseUrl + url,
                params: params,
                timeout: 30000,
            }).then(checkStatus).then(checkCode);
        },
        patch(url, data) {
            console.log(qs.stringify(data));
            return axios({
                method: 'patch',
                url: baseUrl + url,
                data: qs.stringify(data),
                timeout: 30000,
            }).then(checkStatus).then(checkCode);
        },
        delete(url) {
            return axios({
                method: 'delete',
                url: baseUrl + url,
                timeout: 30000,
            }).then(checkStatus).then(checkCode);
        },
    };
