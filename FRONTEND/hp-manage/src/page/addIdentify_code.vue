<template>
    <div class="fillcontain">
        <head-top></head-top>
        <h2 style="font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;
                    padding-left: 10%;padding-top: 20px;font-weight: normal">
            {{title}}
        </h2>
        <el-form :model="selectTable" :rules="rules" ref="selectTable" style="padding-top: 10px;padding-left:10%">
            <el-form-item label="名称" label-width="100px" prop="bid_name">
                <el-col :span="12">
                    <el-input v-model="selectTable.bid_name" auto-complete="off"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="购买日期" label-width="100px">
                <el-col :span="12">
                    <el-form-item prop="purchase_date">
                        <el-date-picker type="date" placeholder="选择日期" v-model="selectTable.purchase_date"
                                        style="width: 100%;"></el-date-picker>
                    </el-form-item>
                </el-col>
            </el-form-item>
            <el-form-item label="过期时间" label-width="100px">
                <el-col :span="12">
                    <el-form-item prop="expired_date">
                        <el-date-picker type="date" placeholder="选择日期"
                                        v-model="selectTable.expired_date"
                                        style="width: 100%;"></el-date-picker>
                    </el-form-item>
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
    import {addIdentify_code} from '@/api/hpData';
    import {mapState, mapActions} from 'vuex';
    import headTop from '@/components/headTop';

    export default {
        name: 'addICode',
        data() {
            return {
                title: '创建激活码',
                selectTable: Object.assign({}, this.$store.state.codetable),
                rules: {
                    bid_name: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 2, max: 6, message: '长度在 2 到 6 个字符', trigger: 'blur'}
                    ],
                    purchase_date: [
                        {type: 'date', required: true, message: '请选择日期', trigger: 'change'}
                    ],
                    expired_date: [
                        {type: 'date', required: true, message: '请选择日期', trigger: 'change'}
                    ],
                }
            };
        },
        watch: {
            selectTable: {
                handler(value, oldValue) {
                    let copiedValue = Object.assign({}, value);
                    this.$store.commit('ADDCODE', copiedValue)
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
            ...mapActions(['addCode']),
            async updateData() {
                let data = Object.assign({}, this.selectTable);
                data.expired_date = this.selectTable.expired_date.ymd();
                data.purchase_date = this.selectTable.purchase_date.ymd();
                const res = await addIdentify_code(data);
                if (res.status === 200) {
                    this.$message({
                        type: 'success',
                        message: '创建激活码信息成功'
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
                        this.addCode(this.selectTable);
                        this.updateData();
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetData() {
                this.selectTable = this.codetable;
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
