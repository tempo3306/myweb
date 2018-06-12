<template>
    <div class="header_container">
        <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/manage' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-for="(item, index) in $route.meta.nav" :key="index">{{item}}</el-breadcrumb-item>

        </el-breadcrumb>
        <el-dropdown @command="handleCommand" menu-align='start'>
            <img :src="baseImgPath + imgpath" class="avator">
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="home">首页</el-dropdown-item>
                <el-dropdown-item command="singout">退出</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
    </div>
</template>

<script>
    import {baseImgPath} from '@/config/env';
    import * as types from '@/store/types';

    export default {
        data() {
            return {
                baseImgPath,
                imgpath: 'boy.jpg'
            };
        },
        created() {
            // if (!this.adminInfo.id) {
            // 	this.getAdminData()
            // }
        },
        computed: {
            // ...mapState(['adminInfo']),
        },
        methods: {
            // ...mapActions(['getAdminData']),
            async handleCommand(command) {
                if (command == 'home') {
                    this.$router.push('/manage');
                } else if (command == 'singout') {
                    this.$store.commit(types.LOGOUT);
                    this.$router.push('/');
                }
            }
        },
    };
</script>

<style lang="less">
    @import '../style/mixin';

    .header_container {
        background-color: #EFF2F7;
        height: 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-left: 20px;
    }

    .avator {
        .wh(36px, 36px);
        border-radius: 50%;
        margin-right: 37px;
    }

    .el-dropdown-menu__item {
        text-align: center;
    }
</style>
