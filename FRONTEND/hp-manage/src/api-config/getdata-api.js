import req from '../api-config/axios-api';

/**
 * 拼团详情
 */
export const groupDetail = param => {
    return req.get('/RestHome/GroupDetail', param);
};
