<template>
    <div>
        <head-top></head-top>
        <section class="data_section">
            <header class="section_title">数据统计</header>
            <el-row :gutter="20" style="margin-bottom: 10px;">
                <el-col :span="4">
                    <div class="data_list today_head"><span class="data_num head">当日数据：</span></div>
                </el-col>
                <el-col :span="4">
                    <div class="data_list"><span class="data_num">{{handerCount}}</span> 新增拍手</div>
                </el-col>
                <el-col :span="4">
                    <div class="data_list"><span class="data_num">{{auctionCount}}</span> 新增标书</div>
                </el-col>
                <el-col :span="4">
                    <div class="data_list"><span class="data_num">{{adminCount}}</span> 新增管理员</div>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="4">
                    <div class="data_list all_head"><span class="data_num head">总数据：</span></div>
                </el-col>
                <el-col :span="4">
                    <div class="data_list"><span class="data_num">{{allhanderCount}}</span> 注册用户</div>
                </el-col>
                <el-col :span="4">
                    <div class="data_list"><span class="data_num">{{allauctionCount}}</span> 订单</div>
                </el-col>
                <el-col :span="4">
                    <div class="data_list"><span class="data_num">{{alladminCount}}</span> 管理员</div>
                </el-col>
            </el-row>
        </section>
        <tendency :sevenDate='sevenDate' :sevenDay='sevenDay'></tendency>
    </div>
</template>

<script>
    import headTop from '../components/headTop';
    import tendency from '../components/tendency';
    import dtime from 'time-formater';
    import {HanderCount, AuctionCount, Identify_codeCount, AdminCount,
        AllhanderCount, AllauctionCount, Allidentify_codeCount, AlladminCount} from '@/api/hpData';

    export default {
        data() {
            return {
                handerCount: null,
                auctionCount: null,
                identify_codeCount: null,
                adminCount: null,
                allhanderCount: null,
                allauctionCount: null,
                allidentify_codeCount: null,
                alladminCount: null,

                sevenDay: [],
                sevenDate: [[], [], []],
            };
        },
        components: {
            headTop,
            tendency,
        },
        mounted() {
            this.initData();
            for (let i = 6; i > -1; i--) {
                const date = dtime(new Date().getTime() - 86400000 * i).format('YYYY-MM-DD');
                this.sevenDay.push(date);
            }
            this.getSevenData();
        },
        computed: {},
        methods: {
            async initData() {
                const today = dtime().format('YYYY-MM-DD');
                Promise.all([HanderCount(today), AuctionCount(today), Identify_codeCount(today), AdminCount(today),
                    AllhanderCount(), AllauctionCount(), Allidentify_codeCount(), AlladminCount()])
                    .then(res => {
                        this.handerCount = res[0].data.count;
                        this.auctionCount = res[1].data.count;
                        this.identify_codeCount = res[2].data.count;
                        this.adminCount = res[3].data.count;
                        this.allhanderCount = res[4].data.count;
                        this.allauctionCount = res[5].data.count;
                        this.allidentify_codeCount = res[6].data.count;
                        this.alladminCount = res[7].data.count;
                    }).catch(err => {
                    console.log(err);
                });
            },
            async getSevenData() {
                const apiArr = [[], [], []];
                this.sevenDay.forEach(item => {
                    apiArr[0].push(HanderCount(item));
                    apiArr[1].push(AuctionCount(item));
                    apiArr[2].push(AdminCount(item));
                });
                const promiseArr = [...apiArr[0], ...apiArr[1], ...apiArr[2]];
                Promise.all(promiseArr).then(res => {
                    const resArr = [[], [], []];
                    res.forEach((item, index) => {
                        if (item.status == 1) {
                            resArr[Math.floor(index / 7)].push(item.count);
                        }
                    });
                    this.sevenDate = resArr;
                }).catch(err => {
                    console.log(err);
                });
            }
        }
    };
</script>

<style lang="less">
    @import '../style/mixin';

    .data_section {
        padding: 20px;
        margin-bottom: 40px;
        .section_title {
            text-align: center;
            font-size: 30px;
            margin-bottom: 10px;
        }
        .data_list {
            text-align: center;
            font-size: 14px;
            color: #666;
            border-radius: 6px;
            background: #E5E9F2;
            .data_num {
                color: #333;
                font-size: 26px;

            }
            .head {
                border-radius: 6px;
                font-size: 22px;
                padding: 4px 0;
                color: #fff;
                display: inline-block;
            }
        }
        .today_head {
            background: #FF9800;
        }
        .all_head {
            background: #20A0FF;
        }
    }

    .wan {
        .sc(16px, #333)
    }
</style>
