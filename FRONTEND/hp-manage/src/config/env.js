/**
 * 配置编译环境和线上环境之间的切换
 *
 * baseUrl: 域名地址
 * routerMode: 路由模式
 * baseImgPath: 图片存放地址
 *
 */
let baseUrl = '//127.0.0.1:8000';
let routerMode = 'hash';
let baseImgPath;


if (process.env.NODE_ENV == 'development') {
	baseUrl = '//127.0.0.1:8000';
    baseImgPath = '//127.0.0.1:8000/media/user_image/';
}else{
    baseUrl = '//127.0.0.1:8000';
    baseImgPath = '/media/user_image/';
}

// baseUrl = '';
// baseImgPath = '/img/';



export {
	baseUrl,
	routerMode,
	baseImgPath
}
