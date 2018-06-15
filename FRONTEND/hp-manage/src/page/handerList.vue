<template>
    <div class="fillcontain">
        <head-top></head-top>
        <div class="table_container" style="padding-top: 10px">
            <div class="filter-container" style="padding-bottom: 45px">
                <el-button class="filter-item" type="primary" :loading="downloadLoading"
                           style="margin-left: 10px; float: right"
                            icon="el-icon-download" @click="handleDownload">导出
                </el-button>
                <el-select @change='handleFilter' style="width: 140px;float: right" class="filter-item"
                           v-model="listQuery.sort">
                    <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key">
                    </el-option>
                </el-select>
                <el-input @keyup.enter.native="handleFilter" style="width: 140px;float: right" class="filter-item"
                          :placeholder="label.search" v-model="listQuery.search">
                </el-input>
                <!--<el-button type="primary" icon="el-icon-delete"></el-button>-->
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
                            <el-form-item label="拍手姓名">
                                <span>{{ props.row.hander_name }}</span>
                            </el-form-item>
                            <el-form-item label="底薪">
                                <span>{{ props.row.basic_salary }}</span>
                            </el-form-item>
                            <el-form-item label="累计收入">
                                <span>{{ props.row.total_income }}</span>
                            </el-form-item>
                        </el-form>
                    </template>
                </el-table-column>
                <el-table-column
                    label="ID"
                    prop="id">
                </el-table-column>
                <el-table-column
                    label="拍手姓名"
                    prop="hander_name">
                </el-table-column>
                <el-table-column
                    label="底薪"
                    prop="basic_salary">
                </el-table-column>
                <el-table-column
                    label="累计收入"
                    prop="total_income">
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
            <el-dialog title="修改拍手信息" width="30%" v-model="dialogFormVisible">
                <el-form :model="selectTable" :rules="rules" ref="selectTable">
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
        getHander,
        addHander,
        updateHander,
        deleteHander,
    } from '@/api/hpData';
    import waves from '@/directive/waves'; // 水波纹指令

    export default {
        // directives: {
        //     waves
        // },
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
                sortOptions: [{label: '底薪 +', key: 'basic_salary'}, {label: '累计收入 +', key: 'total_income'},
                    {label: '底薪 -', key: '-basic_salary'}, {label: '累计收入 -', key: '-total_income'},
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
                    this.getHander();

                } catch (err) {
                    console.log('获取数据失败', err);
                }
            },
            async getHander() {
                console.log(this.listQuery);
                const handers = await getHander({
                    page: this.listQuery.page, limit: this.listQuery.limit,
                    format: 'json', search: this.listQuery.search, sort: this.listQuery.sort
                });
                if (handers.status >= 400) {
                    this.$router.push('login');
                }
                else if (handers.status === 200) ;
                {
                    this.tableData = [];
                    this.count = handers.data.count;
                    handers.data.rows.forEach(item => {
                        const tableData = {};
                        tableData.id = item.id;
                        tableData.hander_name = item.hander_name;
                        tableData.basic_salary = item.basic_salary;
                        tableData.total_income = item.total_income;
                        this.tableData.push(tableData);
                    });
                    console.log(this.tableData);
                }
            },
            handleSizeChange(val) {
                this.listQuery.limit = val;
                this.listQuery.page = 1;
                this.getHander();
            },
            handleCurrentChange(val) {
                this.listQuery.page = val;
                this.getHander();
            },
            handleFilter() {
                this.listQuery.page = 1;
                this.getHander();
            },
            handleRefresh() {
                this.getHander();
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
                this.$router.push({path: 'addHander'});
                // this.selectTable = Object.assign({}, row); //深拷贝
                // this.dialogFormVisible = true;  //弹出对话框
            },
            async handleDelete(index, row) {
                try {
                    const res = await deleteHander(row.id);
                    if (res.status === 200) {
                        this.$message({
                            type: 'success',
                            message: '删除拍手成功'
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
                    console.log('删除拍手失败');
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
                    const res = await updateHander(this.selectTable.id, this.selectTable);
                    console.log(res.status);
                    if (res.status === 200) {
                        this.$message({
                            type: 'success',
                            message: '更新拍手信息成功'
                        });
                        this.getHander();
                    } else {
                        this.$message({
                            type: 'error',
                            message: res.message
                        });
                    }
                } catch (err) {
                    console.log('更新拍手信息失败', err);
                    this.$message({
                        type: 'error',
                        message: err
                    })
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
