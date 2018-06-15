<template>
    <div class="fillcontain">
        <head-top></head-top>
        <h2 style="font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;
                    padding-left: 10%;padding-top: 20px;font-weight: normal">
            {{title}}
        </h2>
        <el-form :model="selectTable" :rules="rules" ref="selectTable" style="padding-top: 10px;padding-left:10%">
            <el-form-item label="拍手姓名" label-width="100px" prop="hander_name">
                <el-col :span="18">
                    <el-input v-model="selectTable.hander_name" auto-complete="off"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="底薪" label-width="100px" prop="basic_salary">
                <el-col :span="18">
                    <el-input type="number" v-model.number="selectTable.basic_salary" auto-complete="off"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="累计收入" label-width="100px" prop="total_income">
                <el-col :span="18">
                    <el-input  type="number" v-model.number="selectTable.total_income" auto-complete="off"></el-input>
                </el-col>
            </el-form-item>
        </el-form>
        <div slot="footer" class="addfooter">
            <el-button @click="resetData">还原</el-button>
            <el-button type="primary" @click="submitForm('selectTable')">创建</el-button>
        </div>
    </div>
</template>

<script>
    import {postHander} from '@/api/hpData';
    import {mapActions} from 'vuex';
    import headTop from '@/components/headTop';

    export default {
        name: 'addHander',
        data() {
            return {
                title: '创建拍手',
                selectTable: Object.assign({}, this.$store.state.handertable),
                rules: {
                    hander_name: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 2, max: 6, message: '长度在 2 到 6 个字符', trigger: 'blur'}
                    ],
                    basic_salary: [
                        {required: true, message: '请输入正确的底薪'},
                        {type: 'number', min: 10, max: 200, message: '请输入合理的底薪'}
                    ],
                    total_income: [
                        {type: 'number', required: true, message: '请输入正确的累计收入'}
                    ],
                }
            };
        },
        watch: {
            selectTable: {
                handler(value, oldValue) {
                    let copiedValue = Object.assign({}, value);
                    this.$store.commit('ADDHANDER', copiedValue)
                },
                deep: true
            }
        },
        // computed: mapState([
        //     // 映射 this.count 为 store.state.count
        //     'codetable'
        // ]),
        // mounted (){
        //     this.selectTable = this.codetable;  //初始化
        // },
        components: {
            headTop,
        },
        methods: {
            ...mapActions(['addHander']),
            async updateData() {
                const res = await postHander(this.selectTable);
                if (res.status === 200) {
                    this.$message({
                        type: 'success',
                        message: '创建拍手信息成功'
                    });
                } else {
                    this.$message({
                        type: 'error',
                        message: res.message
                    });
                }
            },
            submitForm(formName) {
                console.log(this.selectTable);
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.addHander(this.selectTable);
                        this.updateData();
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetData() {
                this.selectTable = this;
            },
        }
    };
</script>

<style scoped>
    .addfooter {
        float: right;
        padding-right: 42%;
    }
</style>
