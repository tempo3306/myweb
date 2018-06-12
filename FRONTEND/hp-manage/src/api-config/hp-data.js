import ajax from './utils';

async function getJSONAsync(url,  data, method) {
    // await关键词使我们免于写一个.then()
    if (method == 'GET'){
        let res = await ajax({
            url: url,
            method: method,
            params: data,
        });
        return res;
    }
    else if (method == 'POST'){
        let res = await ajax({
            url: url,
            method: method,
            data: data,
        });
        return res;
    }


/**
 * 登陆
 */

// export const login = data => getJSONAsync('/admin/login', data, 'POST');



    // GET请求的结果可以从json变量中得到
    // 我们把结果就像一个普通的同步函数一样返回
}


// import { fetch } from "./http"; //引用fetch.js
// import api from './url'; //引用url.js
//
//
// //查看用户
// export function lookOption(issuer,userId) { //lookOption是你要调用接口的名字，issuer,userId是传进来的参数
//     return fetch({
//         //api.Hallowmas 引用url.js里面的数据
//         url: api.Hallowmas+'/halloween/'+issuer+'/question',
//         method: 'get',//请求方法
//         params:{
//             currentUserId:userId //传过去的参数
//         }
//     })
// }


//
// const http = (url = '', data = {}, type = 'GET') => {
//
//     if (type == 'GET') {
//         axios.get(url, {
//             params: data,
//             // headers: {
//             //     Authorization: 'Bearer {token}'
//             // }
//         })
//             .then(function (response) {
//                 return Promise.resolve(response.data);
//             })
//             .catch(function (error) {
//                 console.log(error);
//                 return Promise.reject(err);
//             });
//     }
// };
//
// export const getIdentify_code = () => http('/api/bid/identify_code_manage', data);

//
// export function myGet(url, params) {
//     let _url = apiUrl + url;
//     return new Promise((resolve, reject) => {
//         axios.get(_url, {params}).then(function (response) {
//             resolve(response.data);
//         })
//             .catch(function (err) {
//                 reject(err);
//             });
//     });
// }
//
// export function myPost(url, params) {
//     let _url = apiUrl + url;
//     return new Promise((resolve, reject) => {
//         axios.post(_url, {params}).then(function (response) {
//             resolve(response.data);
//         })
//             .catch(function (err) {
//                 reject(err);
//             });
//     });
// }
//
//
// //调用
// const url = 'school/getNewsInfo' < br >
// // const params = Object.assign({}, commonParams, {
// //   'stuId': 1,
// //   'begin': '1'
// // })
// const params = {
//     'stuId': 1,
//     'begin': '1'
// };
// // 直接返回的promise对象是无法获取其中的值的
// console.log(myGet(url, params));
// // 这个调用promise对象的then方法就可以获取其中的值
// myGet(url, params).then((res) => {
//     if (res.code === ERR_OK) {
//         console.log(res.data);
//     }
// }, (err) => {
//     console.log(err);
// });
//
// const url2 = 'school/getNewsInfoDetail';
// const params2 = {
//     'id': 1
// };
// myPost(url2, params2).then((res) => {
//     if (res.code === ERR_OK) {
//         console.log('success');
//     }
// }, (err) => {
//     console.log(err);
// });


// async / await version (created() becomes async created())
//
// try {
//   const response = await axios.get(`http://jsonplaceholder.typicode.com/posts`)
//   this.posts = response.data
// } catch (e) {
//   this.errors.push(e)
// }
