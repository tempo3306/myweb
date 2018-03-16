function initTable() {
    //先销毁表格
    $('#table').bootstrapTable('destroy');
    //初始化表格,动态从服务器加载数据
    $("#table").bootstrapTable({
        method: "get",  //使用get请求到服务器获取数据
        url: "../api/bid/auction_serverside", //获取数据的Servlet地址
        striped: true,  //表格显示条纹
        pagination: true, //启动分页
        pageSize: 10,  //每页显示的记录数
        pageNumber: 1, //当前第几页
        pageList: [5, 10, 15, 20, 25],  //记录数可选列表
        search: true,  //是否启用查询
        showColumns: true,  //显示下拉框勾选要显示的列
        showRefresh: true,  //显示刷新按钮
        sidePagination: "server", //表示服务端请求
        //设置为undefined可以获取pageNumber，pageSize，searchText，sortName，sortOrder
        //设置为limit可以获取limit, offset, search, sort, order
        queryParamsType: "undefined",
        // columns: createCols(queryParams, ['id','name','price'], hasCheckbox),

        columns: [{
            field: 'id',
            title: 'Item ID'
        }, {
            field: 'description',
            title: '描述'
        }, {
            field: 'auction_name',
            title: '姓名'
        },]

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

$(document).ready(function () {
    //调用函数，初始化表格
    initTable();

    //当点击查询按钮的时候执行
    $("#search").bind("click", initTable);
});


function createBootstrapTable() {
    function init(table, url, params, titles, hasCheckbox, toolbar) {
        $(table).bootstrapTable({
            url: url,                           //请求后台的URL（*）
            method: 'get',                     //请求方式（*）
            toolbar: toolbar,                   //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                    //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: queryParams,           //传递参数（*），这里应该返回一个object，即形如{param1:val1,param2:val2}
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 20,                       //每页的记录行数（*）
            pageList: [20, 50, 100],            //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            //height: 500,                      //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle: true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                  //是否显示父子表

            columns: createCols(params, titles, hasCheckbox),
            data: [{
                id: 1,
                name: 'Item 1',
                price: '$1'
            }, {
                id: 2,
                name: 'Item 2',
                price: '$2'
            }]
        });
    }

    function createCols(params, titles, hasCheckbox) {
        if (params.length != titles.length)
            return null;
        var arr = [];
        if (hasCheckbox) {
            var objc = {};
            objc.checkbox = true;
            arr.push(objc);
        }
        for (var i = 0; i < params.length; i++) {
            var obj = {};
            obj.field = params[i];
            obj.title = titles[i];
            arr.push(obj);
        }
        return arr;
    }

    //可发送给服务端的参数：limit->pageSize,offset->pageNumber,search->searchText,sort->sortName(字段),order->sortOrder('asc'或'desc')
    function queryParams(params) {
        return {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset  //页码
            //name: $("#txt_name").val()//关键字查询
        };
    }

    // 传'#table'
    createBootstrapTable = function (table, url, params, titles, hasCheckbox, toolbar) {
        init(table, url, params, titles, hasCheckbox, toolbar);
    }
}

// createBootstrapTable('#table','',['id','name','price'],['Item ID','Item Name!','Item Price!'],true,'#toolbar');