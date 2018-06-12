/**
 * Created by superman on 17/2/16.
 */
import Vuex from 'vuex'
import Vue from 'vue'
import * as types from './types'

Vue.use(Vuex);
export default new Vuex.Store({
    state: {
        user: {},
        token: null,
        title: ''
    },
    mutations: {
        [types.LOGIN]: (state, data) => {
            localStorage.token = data;
            state.token = data;
            // let t = localStorage.getItem('token');
            // alert(t);
        },
        [types.LOGOUT]: (state) => {
            localStorage.removeItem('token');
            state.token = null;
        },
        [types.TITLE]: (state, data) => {
            state.title = data;
        }
    }
})





// import Vue from 'vue';
// import Vuex from 'vuex';
// import {getAdminInfo} from '@/api/getData';
//
// Vue.use(Vuex);
//
// const state = {
//     adminInfo: {
//         avatar: 'default.jpg'
//     },
// };
//
// const mutations = {
//     saveAdminInfo(state, adminInfo) {
//         state.adminInfo = adminInfo;
//     }
// };
//
// const actions = {
//     async getAdminData({commit}) {
//         console.log("fdsfsf");
//     }
//     //     try {
//     //         const res = await getAdminInfo();
//     //         if (res.status == 1) {
//     //             commit('saveAdminInfo', res.data);
//     //         } else {
//     //             throw new Error(res);
//     //         }
//     //     } catch (err) {
//     //         console.log('您尚未登陆或者session失效');
//     //     }
//     // }
// };
//
// export default new Vuex.Store({
//     state,
//     actions,
//     mutations,
// });
