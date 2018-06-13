import http from '../api/api'

/**
 * 登陆
 */


export const login = (data) => http.post('/api-token-auth/', data);


export const  verify_token = (data) => http.post('/api-token-verify/', data);


export const HanderCount = (data) => http.get('', data);
export const AuctionCount = (data) => http.get('', data);
export const Identify_codeCount = (data) => http.get('', data);
export const AdminCount = (data) => http.get('', data);
export const AllhanderCount = (data) => http.get('', data);
export const AllauctionCount = (data) => http.get('', data);
export const Allidentify_codeCount = (data) => http.get('', data);
export const AlladminCount = (data) => http.get('', data);

export const getIdentify_code = (data) => http.get('/api/bid/ic_manage/', data);
export const deleteIdentify_code = (id) => http.delete('/api/bid/ic_manage/'+id+'/');
export const updateIdentify_code = (id, data) => http.patch('/api/bid/ic_manage/'+id+'/', data);
export const addIdentify_code = (data) => http.post('/api/bid/ic_manage/', data);

export const getCsrftoken = () => http.get('/account/get-token/');
