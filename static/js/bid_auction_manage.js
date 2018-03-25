/**
 * 初始化主表格的事件绑定
 */
var tempdata = []; //当前选中行数据
var tempid = [];
var type = 'add';
var manage_url = "../bid/bid_auction_manage/";

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
                field: 'description',
                title: '描述'
            },
            {
                field: 'auction_name',
                title: '标书姓名'
            },
            {
                field: 'ID_number',
                title: '身份证号'
            },
            {
                field: 'Bid_number',
                title: '标书号'
            },
            {
                field: 'Bid_password',
                title: '标书密码'
            },
            {
                field: 'status',
                title: '状态'
            },
            {
                field: 'count',
                title: '参拍次数'
            },
            {
                field: 'expired_date',
                title: '过期时间'
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


//验证表单
$(document).ready(function () {
    /**
     * 下面是进行插件初始化
     * 你只需传入相应的键值对
     * */
    $('#auction_form').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            /*输入框不同状态，显示图片的样式*/
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            /*验证*/
            description: {
                /*键名username和input name值对应*/
                message: '无效的说明',
                validators: {
                    notEmpty: {
                        /*非空提示*/
                        message: '标书说明不能为空'
                    },
                    stringLength: {
                        /*长度提示*/
                        min: 2,
                        max: 30,
                        message: '用户名长度必须在2到30之间'
                    }/*最后一个没有逗号*/
                }
            },
            auction_name: {
                /*键名username和input name值对应*/
                message: '无效的标书姓名',
                validators: {
                    notEmpty: {
                        /*非空提示*/
                        message: '标书说明不能为空'
                    },
                    stringLength: {
                        /*长度提示*/
                        min: 2,
                        max: 4,
                        message: '用户名长度必须在2到4之间'
                    }/*最后一个没有逗号*/
                }
            },
            ID_number: {
                /*键名username和input name值对应*/
                message: '无效的身份证号',
                validators: {
                    notEmpty: {
                        /*非空提示*/
                        message: '身份证号不能为空'
                    },
                    regexp: {//正则验证
                        regexp: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/,  //身份证号15位，18位
                        message: '所输入的身份证号不符要求'
                    },
                }
            },
            Bid_number: {
                /*键名username和input name值对应*/
                message: '无效的标书号',
                validators: {
                    notEmpty: {
                        /*非空提示*/
                        message: '标书号不能为空'
                    },
                    regexp: {//正则验证
                        regexp: /^\d{8}$/,  //8位数字
                        message: '所输入的标书号不符要求'
                    },
                }
            },
            Bid_password: {
                /*键名username和input name值对应*/
                message: '无效的标书密码',
                validators: {
                    notEmpty: {
                        /*非空提示*/
                        message: '标书密码不能为空'
                    },
                    regexp: {//正则验证
                        regexp: /^\d{4}$/,  //8位数字
                        message: '所输入的标书密码不符要求'
                    },
                }
            },
        },
    });
});


//实现增删改查
$('#btn_add').on('click', function () {
    // $('#description').val('');
    // $('#auction_name').val('');
    // $('#ID_number').val('');
    // $('#Bid_number').val('');
    // $('#Bid_password').val('');
    // $('#status').val('');
    // $('#count').val('');
    // $('#expired_date').val('');
    $('#auctionModal').modal();
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
        $('#auction_name').val(tempdata['auction_name']);
        $('#ID_number').val(tempdata['ID_number']);
        $('#Bid_number').val(tempdata['Bid_number']);
        $('#Bid_password').val(tempdata['Bid_password']);
        $('#status').val(tempdata['status']);
        $('#count').val(tempdata['count']);
        $('#expired_date').val(tempdata['expired_date']);
        type = 'edit'; //添加窗口
        $('#auctionModal').modal();
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
        $('#auctionModal').close;
        initTable();
        // location.reload();
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
    });
});


$("#confirm").click(function () {
    var bv = $("#auction_form").data('bootstrapValidator');
    bv.validate();
    if (bv.isValid()) {
        var id = tempdata['id'];
        alert("yes");//验证成功后的操作，如ajax
        if (type == 'edit') {
            tempdata = $('#auction_form').serialize();
            count = $('#count').val();
            $.ajax({
                url: manage_url + "?id=" + id + '&' + tempdata + '&count=' + count,
                method: 'put',
            }).success(function (data, textStatus, jqXHR) {
                initTable();
            }).error(function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR)
            });
        }
        else if (type == 'add') {
            tempdata = $('#auction_form').serialize();
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


function getschoolList() {//获取下拉学校列表
    $.ajax({
        url: "/eschool/viewEschoolList",//写你自己的方法，返回map，我返回的map包含了两个属性：data：集合，total：集合记录数量，所以后边会有data.data的写法。。。
// 数据发送方式
        type: "get",
// 接受数据格式
        dataType: "json",
// 要传递的数据
        data: 'data',
// 回调函数，接受服务器端返回给客户端的值，即result值
        success: function (data) {
//alert(data.data);

            $.each(data.data, function (i) {
//                    alert(i);
//                    $("<option value='" + data.data[i].schoolno + "'>" + data.data[i].schoolname + "</option>")
//                        .appendTo("#schoolno.selectpicker");
                $('#schoolno.selectpicker').append("<option value=" + data.data[i].schoolno + ">" + data.data[i].schoolname + "</option>");
            });
            $('#schoolno').selectpicker('refresh');

        },

        error: function (data) {

            alert("查询学校失败" + data);

        }
    })

}


///日期
$(".form_datetime").datetimepicker({
    format: 'yyyy-mm-dd',//显示格式
    todayHighlight: 1,//今天高亮
    minView: "month",//设置只显示到月份
    startView: 2,
    forceParse: 0,
    showMeridian: 1,
    autoclose: 1//选择后自动关闭
});


/////参考


$(function () {
    $("#form-test").bootstrapValidator({
        live: 'disabled',//验证时机，enabled是内容有变化就验证（默认），disabled和submitted是提交再验证
        excluded: [':disabled', ':hidden', ':not(:visible)'],//排除无需验证的控件，比如被禁用的或者被隐藏的
        submitButtons: '#btn-test',//指定提交按钮，如果验证失败则变成disabled，但我没试成功，反而加了这句话非submit按钮也会提交到action指定页面
        message: '通用的验证失败消息',//好像从来没出现过
        feedbackIcons: {//根据验证结果显示的各种图标
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            text: {
                validators: {
                    notEmpty: {//检测非空,radio也可用
                        message: '文本框必须输入'
                    },
                    stringLength: {//检测长度
                        min: 6,
                        max: 30,
                        message: '长度必须在6-30之间'
                    },
                    regexp: {//正则验证
                        regexp: /^[a-zA-Z0-9_\.]+$/,
                        message: '所输入的字符不符要求'
                    },
                    remote: {//将内容发送至指定页面验证，返回验证结果，比如查询用户名是否存在
                        url: '指定页面',
                        message: 'The username is not available'
                    },
                    different: {//与指定文本框比较内容相同
                        field: '指定文本框name',
                        message: '不能与指定文本框内容相同'
                    },
                    emailAddress: {//验证email地址
                        message: '不是正确的email地址'
                    },
                    identical: {//与指定控件内容比较是否相同，比如两次密码不一致
                        field: 'confirmPassword',//指定控件name
                        message: '输入的内容不一致'
                    },
                    date: {//验证指定的日期格式
                        format: 'YYYY/MM/DD',
                        message: '日期格式不正确'
                    },
                    choice: {//check控件选择的数量
                        min: 2,
                        max: 4,
                        message: '必须选择2-4个选项'
                    }
                }
            }
        }
    });
    $("#btn-test").click(function () {//非submit按钮点击后进行验证，如果是submit则无需此句直接验证
        $("#form-test").bootstrapValidator('validate');//提交验证
        if ($("#form-test").data('bootstrapValidator').isValid()) {//获取验证结果，如果成功，执行下面代码
            alert("yes");//验证成功后的操作，如ajax
        }
    });
});




