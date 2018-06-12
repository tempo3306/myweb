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

export const getIdentify_code = (data) => http.get('/api/bid/identify_code_manage', data);
export const deleteIdentify_code = (data) => http.delete('/api/bid/identify_code_manage', data);
export const updateIdentify_code = (data) => http.put('/api/bid/identify_code_manage', data);
export const addIdentify_code = (data) => http.post('/api/bid/identify_code_manage', data);
