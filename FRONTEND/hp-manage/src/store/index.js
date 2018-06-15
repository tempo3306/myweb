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
        title: '',
        codetable: {
            'expired_date': new Date(),
            'purchase_date': new Date(),
            'bid_name': '',
        },
        handertable: {
            'hander_name': '',
            'basic_salary': 0,
            'total_income': '',
        },
    },
    mutations: {
        [types.LOGIN]: (state, data) => {
            localStorage.token = data;
            state.token = data;
        },
        [types.LOGOUT]: (state) => {
            localStorage.removeItem('token');
            state.token = null
        },
        [types.TITLE]: (state, data) => {
            state.title = data;
            state.title = data;
        },

        ADDCODE(state, data) {
            let tem = JSON.stringify(data);
            localStorage.codetable = tem;
            console.log(data);
            state.codetable = data;
        },
        ADDHANDER(state, data) {
            let tem = JSON.stringify(data);
            localStorage.handertable = tem;
            state.handertable = data;
        },
    },
    actions: {
        resetadd(context, data){
            if (data.codetable){
                context.commit("ADDCODE", data.codetable);
            }
            if (data.handertable){
                context.commit("ADDHANDER", data.handertable);
            }
        },
        addCode(context, tem){
            context.commit("ADDCODE", tem)
        },
        addHander(context, tem){
            context.commit("ADDHANDER", tem)
        }
    }
})
