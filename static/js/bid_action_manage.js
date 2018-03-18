/**
 * 初始化主表格的事件绑定
 */
var tempdata = []; //当前选中行数据
var tempid = [];
var type = 'add';
var manage_url = "../bid/bid_action_manage/";

function initTable() {
    //先销毁表格
    $('#table').bootstrapTable('destroy');
    //初始化表格,动态从服务器加载数据
    $("#table").bootstrapTable({
        method: "get",  //使用get请求到服务器获取数据
        url: manage_url, //获取数据的地址
        striped: true,  //表格显示条纹
        height: 800,
        toolbar: "#toolbar",                   //工具按钮用哪个容器
        pagination: true, //启动分页
        pageSize: 10,  //每页显示的记录数
        pageNumber: 1, //当前第几页
        pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        search: true,  //是否启用查询
        showColumns: true,  //显示下拉框勾选要显示的列
        showRefresh: true,  //显示刷新按钮
        sidePagination: "server", //表示服务端请求
        //设置为undefined可以获取pageNumber，pageSize，searchText，sortName，sortOrder
        //设置为limit可以获取limit, offset, search, sort, order
        queryParamsType: "undefined",
        clickToSelect: true, //设置 true 将在点击行时，自动选择 rediobox 和 checkbox。
        uniqueId: "id",                     //每一行的唯一标识，一般为主键列
        detailView: 'true',


        // exportDataType: 'all',
        // showExport: true,
        // export: 'glyphicon-export icon-share',  //导出
        columns: [
            {checkbox: true},  //选择器
            {
                field: 'id',
                title: 'ID',
                sortable: true,
            },
            {
                field: 'diff',
                title: '加价幅度'
            },
            {
                field: 'refer_time',
                title: '加价参考时间'
            },
            {
                field: 'bid_time',
                title: '截止时间'
            },
            {
                field: 'delay_time',
                title: '出价延迟时间'
            },
            {
                field: 'ahead_price',
                title: '出价提前价格'
            },
            {
                field: 'hander_id',
                title: '对应拍手'
            },
            {
                field: 'action_date',
                title: '拍牌时间'
            },
            {
                field: 'auction_id',
                title: '标书'
            },
            {
                field: 'action_result',
                title: '结果记录'
            },
        ]

        // queryParams: function queryParams(params) {   //设置查询参数
        //     var param = {
        //         pageNumber: params.pageNumber,
        //         pageSize: params.pageSize,
        //         orderNum: $("#orderNum").val()
        //     };
        //     return param;
        // },
        // onLoadSuccess: function () {  //加载成功时执行
        //     layer.msg("加载成功");
        // },
        // onLoadError: function () {  //加载失败时执行
        //     layer.msg("加载数据失败", {time: 1500, icon: 2});
        // }
    });
}


//调用函数，初始化表格
$(document).ready(function () {
    //调用函数，初始化表格
    initTable();
    //当点击查询按钮的时候执行
    $("#search").bind("click", initTable);
});


//实现增删改查
$('#btn_add').on('click', function () {
    // $('#description').val('');
    // $('#action_name').val('');
    // $('#ID_number').val('');
    // $('#Bid_number').val('');
    // $('#Bid_password').val('');
    // $('#status').val('');
    // $('#count').val('');
    // $('#expired_date').val('');
    $('#actionModal').modal();
    type = 'add'; //添加窗口
});

$('#btn_edit').on('click', function () {
    tempdata = $('#table').bootstrapTable('getSelections'); //获取获取删除的表单
    if (tempdata === undefined || tempdata.length == 0) {  //未选择
        $('#noselection_warning').modal();
    }
    else if (tempdata.length > 1) {
        $('#toomuch_selection_warning').modal();
    }
    else {
        tempdata = tempdata[0];
        $('#description').val(tempdata['description']);
        $('#action_name').val(tempdata['action_name']);
        $('#ID_number').val(tempdata['ID_number']);
        $('#Bid_number').val(tempdata['Bid_number']);
        $('#Bid_password').val(tempdata['Bid_password']);
        $('#status').val(tempdata['status']);
        $('#count').val(tempdata['count']);
        $('#expired_date').val(tempdata['expired_date']);
        type = 'edit'; //添加窗口
        $('#actionModal').modal();
    }
});

$('#btn_delete').on('click', function () {
    tempdata = $('#table').bootstrapTable('getSelections'); //获取获取删除的表单
    console.log(tempdata);
    if (tempdata === undefined || tempdata.length == 0) {  //未选择
        $('#noselection_warning').modal();
    }
    else {
        $('#delete_confirm').modal();
        tempid = [];
        for (j = 0, len = tempdata.length; j < len; j++) {
            tempid.push(tempdata[j]['id']);
        }
        tempdata = {'id': tempid};
    }
});

$('#delete_confirm').on('click', '#delete', function () {
    tempdata = JSON.stringify(tempdata);
    $.ajax({
        url: manage_url + '?data=' + tempdata, //获取数据的地址
        method: 'DELETE',
    }).success(function (data, textStatus, jqXHR) {
        $('#actionModal').close;
        initTable();
        // location.reload();
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
    });
});


$('#actionModal').on('click', '#confirm', function () {
    var id = tempdata['id'];
    if (type == 'edit') {
        tempdata = $('#action_form').serialize();
        $.ajax({
            url: manage_url + "?id=" + id + '&' + tempdata + '/',
            method: 'put',
        }).success(function (data, textStatus, jqXHR) {
            initTable();
        }).error(function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR)
        });
    }
    else if (type == 'add') {
        tempdata = $('#action_form').serialize();
        $.ajax({
            url: manage_url,
            method: 'post',
            data: tempdata,
        }).success(function (data, textStatus, jqXHR) {
            initTable();
        }).error(function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR)
        });
    }
});

//csrf
$(function () {
    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    });
});

//获取cookie
function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");

    if (arr = document.cookie.match(reg))

        return unescape(arr[2]);
    else
        return null;
}



//
// $.get(url, function (result) {
//         if (result.code=='0000') {
//             var data = {total:result.data.totalCount,rows:result.data.dataList};
//             $table.bootstrapTable({
//                 data:data,
//                 dataType: "json",
//                 // data:json.data.dataList,
//                 cache: false, // 不缓存
//                 // height: getHeight(), // 设置高度，会启用固定表头的特性
//                 striped: true, // 隔行加亮
//                     ...
//             })
//         }
//     }, "json")


