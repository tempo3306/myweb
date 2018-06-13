<template>
    <div class="login_page fillcontain">
        <transition name="form-fade" mode="in-out">
            <section class="form_contianer" v-show="showLogin">
                <div class="manage_tip">
                    <p>elm后台管理系统</p>
                </div>
                <el-form :model="loginForm" :rules="rules" ref="loginForm">
                    <el-form-item prop="username">
                        <el-input v-model="loginForm.username" placeholder="用户名"><span>dsfsf</span></el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <el-input type="password" placeholder="密码" v-model="loginForm.password"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="submitForm('loginForm')" class="submit_btn">登陆</el-button>
                    </el-form-item>
                </el-form>
                <p class="tip">温馨提示：</p>
                <p class="tip">未登录过的新用户，自动注册</p>
                <p class="tip">注册过的用户可凭账号密码登录</p>
            </section>
        </transition>
    </div>
</template>

<script>
    import {login, verify_token} from '@/api/hpData';
    import {mapActions, mapState} from 'vuex';
    import {setToken} from '@/utils/auth';
    import store from '@/store/index';
    import * as types from '@/store/types';
    import {getCsrftoken} from '@/api/hpData';

    export default {
        data() {
            return {
                loginForm: {
                    username: '',
                    password: '',
                },
                rules: {
                    username: [
                        {required: true, message: '请输入用户名', trigger: 'blur'},
                    ],
                    password: [
                        {required: true, message: '请输入密码', trigger: 'blur'}
                    ],
                },
                showLogin: true,
            };
        },

        // mounted  页面元素加载完成后执行，对节点进行一定的操作
        // 登录成功  或者  读取到登录过   this.$router.push('manage');
        created() {
            this.getCsrf();
            this.showLogin = true;
            let token = localStorage.getItem('token') || this.$store.state.token;
            this.autologin(token);
        },
        computed: {
            // ...mapState(['adminInfo']),
        },
        methods: {
            // ...mapActions(['getAdminData']),
            async getCsrf() {
                const res = await getCsrftoken();
                if (res.status === 200) {
                    setToken(res.data.token);
                    console.log(res.data.token);
                }
            },

            async submitForm(formName) {
                this.$refs[formName].validate(async (valid) => {
                    if (valid) {
                        const res = await login({username: this.loginForm.username, password: this.loginForm.password});
                        console.log(res.data);
                        if (res.status == 200) {
                            //弹消息框
                            this.$message({
                                type: 'success',
                                message: '登录成功'
                            });
                            this.$store.commit(types.LOGIN, res.data.token);  //保存token
                            // setToken(res.data.token); //保存登录用的token
                            // this.$router.push('manage');
                            // $route为当前router跳转对象里面可以获取name、path、query、params等
                            // $router为VueRouter实例，想要导航到不同URL，则使用$router.push方法
                            let redirect = decodeURIComponent(this.$route.query.redirect || '/manage');
                            this.$router.push({
                                path: redirect
                            });
                        } else {
                            this.$message({
                                type: 'error',
                                message: res.message
                            });
                        }
                    } else {
                        this.$notify.error({
                            title: '错误',
                            message: '请输入正确的用户名密码',
                            offset: 100
                        });
                        return false;
                    }
                });
            },
            async autologin(token) {
                // alert(token);
                if (token) {
                    const res = await verify_token({'token': token});
                    if (res.status === 200) {
                        this.showLogin = false;
                    }
                    else {
                        // alert('TOKEN无效');
                        this.$store.commit(types.LOGOUT);
                    }
                }
            }
        },
        //watch侦听属性: 当你有一些数据需要随着其它数据变动而变动
        watch: {
            showLogin: function () {
                if (!this.showLogin) {
                    this.$message({
                        type: 'success',
                        message: '检测到您之前登录过，将自动登录'
                    });
                    let redirect = decodeURIComponent(this.$route.query.redirect || '/manage');
                    this.$router.push({
                        path: redirect
                    });
                }
            }
        }
    };
</script>

<style lang="less" scoped>
    @import '../style/mixin';

    .login_page {
        background-color: #324057;
    }

    .manage_tip {
        position: absolute;
        width: 100%;
        top: -100px;
        left: 0;
        p {
            font-size: 34px;
            color: #fff;
        }
    }

    .form_contianer {
        .wh(320px, 210px);
        .ctp(320px, 210px);
        padding: 25px;
        border-radius: 5px;
        text-align: center;
        background-color: #fff;
        .submit_btn {
            width: 100%;
            font-size: 16px;
        }
    }

    .tip {
        font-size: 12px;
        color: red;
    }

    .form-fade-enter-active, .form-fade-leave-active {
        transition: all 1s;
    }

    .form-fade-enter, .form-fade-leave-active {
        transform: translate3d(0, -50px, 0);
        opacity: 0;
    }
</style>
