<!-- 左侧控制面板 -->
<template>
	<div class="manage_page fillcontain">
		<el-row style="height: 100%;">
	  		<el-col :span="4"  style="min-height: 100%; background-color: #324057;">
                <!-- 添加router 启用vue-router 这种模式-->
				<el-menu :default-active="defaultActive" style="min-height: 100%;" theme="dark" router>
					<el-menu-item index="manage"><i class="el-icon-menu"></i>首页</el-menu-item>
					<el-submenu index="2">
						<template slot="title"><i class="el-icon-document"></i>数据管理</template>
						<el-menu-item index="handerList">拍手列表</el-menu-item>
						<el-menu-item index="auctionList">标书列表</el-menu-item>
						<el-menu-item index="userList">策略列表</el-menu-item>
                        <el-menu-item index="identify_codeList">激活码列表</el-menu-item>
					</el-submenu>
					<el-submenu index="3">
						<template slot="title"><i class="el-icon-plus"></i>添加数据</template>
                        <!--index属性直接书写的路由-->
                        <el-menu-item index="addHander">添加拍手</el-menu-item>
                        <el-menu-item index="addAuction">添加标书</el-menu-item>
                        <el-menu-item index="addAction">添加策略</el-menu-item>
                        <el-menu-item index="addIdentify_code">添加激活码</el-menu-item>
					</el-submenu>
					<!--<el-submenu index="4">-->
						<!--<template slot="title"><i class="el-icon-star-on"></i>图表</template>-->
						<!--<el-menu-item index="visitor">用户分布</el-menu-item>-->
						<!--&lt;!&ndash; <el-menu-item index="newMember">用户数据</el-menu-item> &ndash;&gt;-->
					<!--</el-submenu>-->
					<!--<el-submenu index="5">-->
						<!--<template slot="title"><i class="el-icon-edit"></i>编辑</template>-->
						<!--&lt;!&ndash; <el-menu-item index="uploadImg">上传图片</el-menu-item> &ndash;&gt;-->
						<!--<el-menu-item index="vueEdit">文本编辑</el-menu-item>-->
					<!--</el-submenu>-->
					<el-submenu index="4">
						<template slot="title"><i class="el-icon-setting"></i>设置</template>
						<el-menu-item index="adminSet">管理员设置</el-menu-item>
						<!-- <el-menu-item index="sendMessage">发送通知</el-menu-item> -->
					</el-submenu>
					<el-submenu index="5">
						<template slot="title"><i class="el-icon-warning"></i>说明</template>
						<el-menu-item index="explain">说明</el-menu-item>
					</el-submenu>
				</el-menu>
			</el-col>
			<el-col :span="20" style="height: 100%;overflow: auto;">
                <keep-alive> <!-- 用来缓存组件,避免多次加载相应的组件,减少性能消耗 -->
                    <!-- 组件将被缓存 -->
                    <router-view></router-view>
				</keep-alive>
			</el-col>
		</el-row>
  	</div>
</template>

<script>
    export default {
		computed: {
		    //defaultActive 当前激活菜单的 index
            //每次渲染menu都会读当前path 设置为default-active
			defaultActive: function(){
				return this.$route.path.replace('/', '');
			}
		},
    }
</script>


<style lang="less" scoped>
	@import '../style/mixin';
	.manage_page{

	}

</style>
