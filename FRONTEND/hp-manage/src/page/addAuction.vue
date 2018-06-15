<template>
    <div class="fillcontain">
        <head-top></head-top>
        <h2 style="font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;
                    padding-left: 10%;padding-top: 20px;font-weight: normal">
            {{title}}
        </h2>
        <el-form :model="selectTable" :rules="rules" ref="selectTable" style="padding-top: 10px;padding-left:10%">
            <el-form-item label="标书说明" label-width="100px" prop="description">
                <el-col :span="18">
                    <el-input v-model="selectTable.description" auto-complete="off"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="标书姓名" label-width="100px" prop="auction_name">
                <el-col :span="18">
                    <el-input v-model="selectTable.auction_name" auto-complete="off"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="身份证号" label-width="100px" prop="ID_number">
                <el-col :span="18">
                    <el-input v-model="selectTable.ID_number" auto-complete="off"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="标书号" label-width="100px" prop="Bid_number">
                <el-col :span="18">
                    <el-input v-model="selectTable.Bid_number" auto-complete="off"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="标书密码" label-width="100px" prop="Bid_password">
                <el-col :span="18">
                    <el-input  v-model="selectTable.Bid_password" auto-complete="off"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="标书状态" label-width="100px" prop="status">
                <el-col :span="18">
                    <el-select class="filter-item" v-model="selectTable.status">
                        <el-option v-for="item in statusOptions" :key="item.key" :label="item.label"
                                   :value="item.key">
                        </el-option>
                    </el-select>
                </el-col>
            </el-form-item>
            <el-form-item label="参拍次数" label-width="100px" prop="count">
                <el-col :span="18">
                    <el-input v-model.number="selectTable.count" auto-complete="off"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="过期时间" label-width="100px">
                <el-col :span="18">
                    <el-form-item prop="expired_date">
                        <el-date-picker type="date" placeholder="选择日期" v-model="selectTable.expired_date"
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
    import {postAuction} from '@/api/hpData';
    import {mapState, mapActions} from 'vuex';
    import headTop from '@/components/headTop';

    export default {
        name: 'addAuction',

        data() {
            const checkId_number = (rule, value, callback) => {
                let reg = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
                if(reg.test(value) === false){
                    return callback(new Error('请输入正确的身份证号'));
                }
                else{
                    callback();
                }
            };
            const checkBid_number = (rule, value, callback) => {
                let reg = /(^\d{8}$)/;
                if(reg.test(value) === false){
                    return callback(new Error('请输入8位标书号'));
                }
                else{
                    callback();
                }
            };
            const checkBid_password = (rule, value, callback) => {
                let reg = /(^\d{4}$)/;
                if(reg.test(value) === false){
                    return callback(new Error('请输入4位标书密码'));
                }
                else{
                    callback();
                }
            };
            return {
                title: '创建标书',
                selectTable: Object.assign({}, this.$store.state.auctiontable),
                statusOptions: [
                    {label: '未中标结束交易', key: '未中标结束交易'},
                    {label: '中标完成交易', key: '中标完成交易'},
                    {label: '正常进行中', key: '正常进行中'},
                    {label: '标书失效', key: '标书失效'},
                    {label: '中标未完成交易', key: '中标未完成交易'},
                ],
                rules: {
                    description: [
                        {required: true, message: '请输入标书描述', trigger: 'blur'},
                        {min: 2, max: 15, message: '长度在 2 到 15 个字符', trigger: 'blur'}
                    ],
                    auction_name: [
                        {required: true, message: '请输入姓名', trigger: 'blur'},
                        {min: 2, max: 4, message: '长度在 2 到 4 个字符', trigger: 'blur'}
                    ],
                    ID_number: [
                        {validator: checkId_number, trigger: 'blur'}
                    ],
                    Bid_number: [
                        {validator: checkBid_number, trigger: 'blur'}
                    ],
                    Bid_password: [
                        {validator: checkBid_password, trigger: 'blur'}
                    ],
                    count: [
                        {required: true, message: '请输入正确的次数'},
                        {type: 'number', min: 0, max: 6, message: '请输入正确的次数'}
                    ],
                    status: [
                        {required: true, message: '请选择标书状态'}
                    ],
                    expired_date: [
                        {type: 'date', required: true, message: '请选择日期', trigger: 'change'}
                    ],
                },
            };
        },
        watch: {
            selectTable: {
                handler(value, oldValue) {
                    let copiedValue = Object.assign({}, value);
                    this.$store.commit('ADDAUCTION', copiedValue)
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
            ...mapActions(['addAuction']),
            async updateData() {
                let data = Object.assign({}, this.selectTable);
                data.expired_date = this.selectTable.expired_date.ymd();
                delete data.expired_date_str;
                const res = await postAuction(data);
                if (res.status === 200) {
                    this.$message({
                        type: 'success',
                        message: '创建标书信息成功'
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
                        this.addAuction(this.selectTable);
                        console.log("valid");
                        this.updateData();
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetData() {
                this.selectTable = this.auctiontable;
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
