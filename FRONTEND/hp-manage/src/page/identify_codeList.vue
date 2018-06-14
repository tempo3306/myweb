<template>
    <div class="fillcontain">
        <head-top></head-top>
        <div class="table_container" style="padding-top: 10px">
            <div class="filter-container" style="padding-bottom: 45px">
                <el-button class="filter-item" type="primary" :loading="downloadLoading"
                           style="margin-left: 10px; float: right"
                           v-waves icon="el-icon-download" @click="handleDownload">导出
                </el-button>

                <!--<el-select clearable style="width: 90px" class="filter-item" v-model="listQuery.importance"-->
                <!--:placeholder="$t('table.importance')">-->
                <!--<el-option v-for="item in importanceOptions" :key="item" :label="item" :value="item">-->
                <!--</el-option>-->
                <!--</el-select>-->
                <!--<el-select clearable class="filter-item" style="width: 130px" v-model="listQuery.type"-->
                <!--:placeholder="$t('table.type')">-->
                <!--<el-option v-for="item in  calendarTypeOptions" :key="item.key"-->
                <!--:label="item.display_name+'('+item.key+')'" :value="item.key">-->
                <!--</el-option>-->
                <!--</el-select>-->
                <el-select @change='handleFilter' style="width: 140px;float: right" class="filter-item"
                           v-model="listQuery.sort">
                    <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key">
                    </el-option>
                </el-select>
                <el-input @keyup.enter.native="handleFilter" style="width: 200px;" class="filter-item"
                          :placeholder="label.search" v-model="listQuery.search">
                </el-input>

                <!--<el-checkbox class="filter-item" style='margin-left:15px;' @change='tableKey=tableKey+1'-->
                <!--v-model="showReviewer">{{$t('table.reviewer')}}-->
                <!--</el-checkbox>-->
            </div>
            <el-table
                :data="tableData"
                style="width: 100%"
                height="700">   <!--固定表头-->
                <el-table-column type="expand">
                    <template scope="props">
                        <el-form label-position="left" inline class="demo-table-expand">
                            <el-form-item label="ID">
                                <span>{{ props.row.id }}</span>
                            </el-form-item>
                            <el-form-item label="名称">
                                <span>{{ props.row.bid_name }}</span>
                            </el-form-item>
                            <el-form-item label="购买日期">
                                <span>{{ props.row.purchase_date_str }}</span>
                            </el-form-item>
                            <el-form-item label="到期时间">
                                <span>{{ props.row.expired_date_str }}</span>
                            </el-form-item>
                            <el-form-item label="激活码">
                                <span>{{ props.row.identify_code }}</span>
                            </el-form-item>
                        </el-form>
                    </template>
                </el-table-column>
                <el-table-column
                    label="ID"
                    prop="id">
                </el-table-column>
                <el-table-column
                    label="名称"
                    prop="bid_name">
                </el-table-column>
                <el-table-column
                    label="购买日期"
                    prop="purchase_date_str">
                </el-table-column>
                <el-table-column
                    label="到期时间"
                    prop="expired_date_str">
                </el-table-column>
                <el-table-column
                    label="激活码"
                    prop="identify_code">
                </el-table-column>
                <el-table-column label="操作" width="200">
                    <!--scope 对 父元素遍历，scope返回的值是slot标签上返回的所有属性值，并且是一个对象的形式保存起来，获取的是一个对象-->
                    <template scope="scope">
                        <el-button
                            size="mini"
                            @click="handleEdit(scope.$index, scope.row)">编辑
                        </el-button>
                        <el-button
                            size="mini"
                            type="Success"
                            @click="handleAdd(scope.$index, scope.row)">添加
                        </el-button>
                        <el-button
                            size="mini"
                            type="danger"
                            @click="handleDelete(scope.$index, scope.row)">删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="Pagination">
                <el-pagination
                    background
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="listQuery.page"
                    :page-sizes="[10,20,30, 50]"
                    :page-size="listQuery.limit"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="count">
                </el-pagination>
            </div>
            <el-dialog title="修改激活码信息" width="30%" v-model="dialogFormVisible">
                <el-form :model="selectTable" :rules="rules" ref="selectTable">
                    <el-form-item label="名称" label-width="100px" prop="bid_name">
                        <el-col :span="18">
                            <el-input v-model="selectTable.bid_name" auto-complete="off"></el-input>
                        </el-col>
                    </el-form-item>
                    <el-form-item label="购买日期" label-width="100px">
                        <el-col :span="18">
                            <el-form-item prop="purchase_date">
                                <el-date-picker type="date" placeholder="选择日期" v-model="selectTable.purchase_date"
                                                style="width: 100%;"></el-date-picker>
                            </el-form-item>
                        </el-col>
                    </el-form-item>
                    <el-form-item label="过期时间" label-width="100px">
                        <el-col :span="18">
                            <el-form-item prop="expired_date">
                                <el-date-picker type="date" placeholder="选择日期"
                                                v-model="selectTable.expired_date"
                                                style="width: 100%;"></el-date-picker>
                            </el-form-item>
                        </el-col>
                    </el-form-item>
                    <el-form-item label="更换激活码" label-width="100px">
                        <el-col :span="6">
                            <el-switch v-model="change_identify_code"></el-switch>
                        </el-col>
                        <el-col class="line" :span="12">{{'当前激活码: ' + selectTable.identify_code}}</el-col>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="cancelData">取 消</el-button>
                    <el-button type="primary" @click="submitForm('selectTable')">确 定</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    import headTop from '@/components/headTop';
    import {baseUrl, baseImgPath} from '@/config/env';
    import {
        getIdentify_code,
        addIdentify_code,
        updateIdentify_code,
        deleteIdentify_code,
    } from '@/api/hpData';
    import waves from '@/directive/waves'; // 水波纹指令



    export default {
        directives: {
            waves
        },
        data() {
            var checkDate1 = (rule, value, callback) => {
                console.log(value);
                if (!value) {
                    return callback(new Error('年龄不能为空'));
                }
            };
            var checkDate2 = (rule, value, callback) => {
                console.log(value);
                if (!value) {
                    return callback(new Error('年龄不能为空'));
                }
            };

            return {
                baseUrl,
                baseImgPath,
                city: {},
                offset: 0,
                count: 0,
                listQuery: {
                    page: 1,
                    limit: 20,
                    importance: undefined,
                    search: undefined,
                    type: undefined,
                    sort: 'id'
                },
                label: {
                    search: '搜索',
                },
                sortOptions: [{label: '购买日期 +', key: 'purchase_date'}, {label: '到期时间 +', key: 'expired_date'},
                    {label: '购买日期 +', key: '-purchase_date'}, {label: '到期时间 +', key: '-expired_date'},
                    {label: 'id +', key: 'id'}, {label: 'id -', key: '-id'}
                ],
                tableData: [],
                currentPage: 1,
                selectTable: {},
                dialogFormVisible: false,
                categoryOptions: [],
                selectedCategory: [],
                address: {},
                downloadLoading: false,
                change_identify_code: false,

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
                },
            };
        },
        created() {
            this.initData();
        },
        components: {
            headTop,
        },
        methods: {
            async initData() {
                try {
                    this.getIdentify_code();

                } catch (err) {
                    console.log('获取数据失败', err);
                }
            },
            async getIdentify_code() {
                console.log(this.listQuery);
                const identify_codes = await getIdentify_code({
                    page: this.listQuery.page, limit: this.listQuery.limit,
                    format: 'json', search: this.listQuery.search, sort: this.listQuery.sort
                });
                if (identify_codes.status >= 400) {
                    this.$router.push('login');
                }
                else if (identify_codes.status === 200) ;
                {
                    this.tableData = [];
                    this.count = identify_codes.data.count;
                    identify_codes.data.rows.forEach(item => {
                        const tableData = {};
                        tableData.id = item.id;
                        tableData.bid_name = item.bid_name;
                        tableData.purchase_date_str = item.purchase_date;
                        tableData.expired_date_str = item.expired_date;
                        tableData.purchase_date = new Date(item.purchase_date.replace(/-/g, '/'));
                        tableData.expired_date = new Date(item.expired_date.replace(/-/g, '/'));
                        tableData.identify_code = item.identify_code;
                        this.tableData.push(tableData);
                    });
                }
            },
            handleSizeChange(val) {
                this.listQuery.limit = val;
                this.listQuery.page = 1;
                this.getIdentify_code();
            },
            handleCurrentChange(val) {
                this.listQuery.page = val;
                this.getIdentify_code();
            },
            handleFilter() {
                this.listQuery.page = 1;
                this.getIdentify_code();
            },
            handleCreate() {
                // this.resetTemp()
                // this.dialogStatus = 'create'
                // this.dialogFormVisible = true
                // this.$nextTick(() => {
                //     this.$refs['dataForm'].clearValidate()
                // })
            },
            handleDownload() {
                //     this.downloadLoading = true;
                //     import('@/vendor/Export2Excel').then(excel => {
                //         const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
                //         const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
                //         const data = this.formatJson(filterVal, this.list)
                //         excel.export_json_to_excel({
                //             header: tHeader,
                //             data,
                //             filename: 'table-list'
                //         })
                //         this.downloadLoading = false
                //     })
                // },
            },
            submitForm(formName) {
                console.log(this.selectTable);
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.updateData();
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            handleEdit(index, row) {
                this.selectTable = Object.assign({}, row); //深拷贝
                this.dialogFormVisible = true;  //弹出对话框
            },
            handleAdd() {
                this.$router.push({path: 'addIdentify_code'});
                // this.selectTable = Object.assign({}, row); //深拷贝
                // this.dialogFormVisible = true;  //弹出对话框
            },
            async handleDelete(index, row) {
                try {
                    const res = await deleteIdentify_code(row.id);
                    if (res.status === 200) {
                        this.$message({
                            type: 'success',
                            message: '删除激活码成功'
                        });
                        this.tableData.splice(index, 1);
                    } else {
                        this.$message({
                            type: 'error',
                            message: '操作失败'
                        });
                    }
                } catch (err) {
                    this.$message({
                        type: 'error',
                        message: '操作失败'
                    });
                    console.log('删除店铺失败');
                }
            },
            // async querySearchAsync(queryString, cb) {
            //     if (queryString) {
            //         try {
            //             const cityList = await searchplace(this.city.id, queryString);
            //             if (cityList instanceof Array) {
            //                 cityList.map(item => {
            //                     item.value = item.address;
            //                     return item;
            //                 });
            //                 cb(cityList);
            //             }
            //         } catch (err) {
            //             console.log(err);
            //         }
            //     }
            // },
            // handleServiceAvatarScucess(res, file) {
            //     if (res.status == 1) {
            //         this.selectTable.image_path = res.image_path;
            //     } else {
            //         this.$message.error('上传图片失败！');
            //     }
            // },
            // beforeAvatarUpload(file) {
            //     const isRightType = (file.type === 'image/jpeg') || (file.type === 'image/png');
            //     const isLt2M = file.size / 1024 / 1024 < 2;
            //
            //     if (!isRightType) {
            //         this.$message.error('上传头像图片只能是 JPG 格式!');
            //     }
            //     if (!isLt2M) {
            //         this.$message.error('上传头像图片大小不能超过 2MB!');
            //     }
            //     return isRightType && isLt2M;
            // },
            async updateData() {
                this.dialogFormVisible = false;
                try {
                    console.log(this.selectTable);
                    this.selectTable.purchase_date_str = this.selectTable.purchase_date.ymd();
                    this.selectTable.expired_date_str = this.selectTable.expired_date.ymd();
                    this.selectTable.change_identify_code = this.change_identify_code;
                    const res = await updateIdentify_code(this.selectTable.id, this.selectTable);
                    console.log(res.status);
                    if (res.status === 200) {
                        this.$message({
                            type: 'success',
                            message: '更新激活码信息成功'
                        });
                        this.getIdentify_code();
                    } else {
                        this.$message({
                            type: 'error',
                            message: res.message
                        });
                    }
                } catch (err) {
                    console.log('更新激活码信息失败', err);
                }
            },
            cancelData() {
                this.dialogFormVisible = false;
            }
        }
    };


</script>

<style lang="less">
    @import '../style/mixin';

    .demo-table-expand {
        font-size: 0;
    }

    .demo-table-expand label {
        width: 90px;
        color: #99a9bf;
    }

    .demo-table-expand .el-form-item {
        margin-right: 0;
        margin-bottom: 0;
        width: 50%;
    }

    .table_container {
        padding: 20px;
    }

    .Pagination {
        display: flex;
        justify-content: flex-start;
        margin-top: 8px;
    }

    .avatar-uploader .el-upload {
        border: 1px dashed #d9d9d9;
        border-radius: 6px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .avatar-uploader .el-upload:hover {
        border-color: #20a0ff;
    }

    .avatar-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        width: 120px;
        height: 120px;
        line-height: 120px;
        text-align: center;
    }

    .avatar {
        width: 120px;
        height: 120px;
        display: block;
    }

    .el-dialog--small {
        width: 30%;
    }
</style>
