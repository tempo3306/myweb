var answer = '0000';
var question = '';
var yanhtml = '';

var total_right = 0;
var total_question = 0;
var accuracy = 0;
var total_time = 0;
var avarage_time = 0;
var start_time = 0;

var error_list = [];


//浏览器类型判定
function getOs() {
    if (navigator.userAgent.indexOf("MSIE") > 0) {
        return "IE"; //InternetExplor
    }
    else if (isFirefox = navigator.userAgent.indexOf("Firefox") > 0) {
        return "FF"; //firefox
    }
    else if (isSafari = navigator.userAgent.indexOf("Safari") > 0) {
        return "SF"; //Safari
    }
    else if (isCamino = navigator.userAgent.indexOf("Camino") > 0) {
        return "C"; //Camino
    }
    else if (isMozilla = navigator.userAgent.indexOf("Gecko/") > 0) {
        return "G"; //Gecko
    }
    else if (isMozilla = navigator.userAgent.indexOf("Opera") >= 0) {
        return "O"; //opera
    } else {
        return 'Other';
    }
}


//限制只能输入数字
$(function () {
    $('input').keypress(function (e) {
        if (!String.fromCharCode(e.keyCode).match(/[0-9\.]/)) {
            return false;
        }
    })
});

//判定验证码是否回答正确
function Answer(useranswer) {
    if (useranswer == answer) {
        return true
    } else {
        return false
    }
}


//更新验证码及弹出窗口
var id = Math.floor(Math.random() * 3900 + 1);
var path_yanzhengma = "/bid/yanzhengma/" + id;
var path_answer = "/bid/answer/" + id;


//刷新功能
function GetYanzhengma() {
    time1 = new Date().getTime();
    id = Math.floor(Math.random() * 3900 + 1); //全局变量
    var path_yanzhengma = "/bid/yanzhengma/" + id;
    var path_answer = "/bid/answer/" + id;
    $.get(path_answer, null, function (ret) {
        question = ret.question;
        answer = ret.answer;
        $('#question').text(question);
    });  //获取答案和问题
    $("#yanzhengma").load(path_yanzhengma);//加载验证码
}


function Control() {
    switch (mode) {
        case 0: {
            Confirm();
        }
            break;
        case 1: {
            Test();
        }
            break;
        case 2: {
            Examine();
        }
            break;
    }

}

function Confirm() {
    time2 = new Date().getTime();
    usetime = time2 - time1;
    var useranswer = $('input').val();
    var result = Answer(useranswer);

    if (result) {
        GetYanzhengma();  //刷新验证码
        $('input').val("");
        var a = document.getElementsByTagName("input");
        a[0].focus();
        alert("回答正确，用时" + usetime + "毫秒");
    }
    else {
        $('input').val(""); //清空
        // $('input').focus();
        var a = document.getElementsByTagName("input");
        a[0].focus();
        alert("回答错误");

        //          window.setTimeout(function ()
        // {
        //     var a=document.getElementsByTagName("input");
        //         a[0].focus();
        // }, 0);

    }
}


function Test() {
    var useranswer = $('input').val();
    var result = Answer(useranswer);
    if (total_question <= 9) {
        total_question++;
        if (result) {
            total_right++;
        }
        else {
            yanhtml = $(".yanzhengma")[0].src;
            console.log(yanhtml);
            var imgstr = "<img src=" + yanhtml + ">" + "</img>";
            var ua = '';
            useranswer ? ua = useranswer : ua = '空白';
            error_list.push({
                path: imgstr,
                useranswer: ua,
                rightanswer: answer,
                question: question
            })
        }
        console.log(error_list);

        GetYanzhengma();  //刷新验证码
        $('input').val("");
        var a = document.getElementsByTagName("input");
        a[0].focus();
        $('#practicestatus').text('第' + total_question + '/10题');

    }
    else if (total_question === 10) {
        //结束
        create_table(error_list);
        end_time = new Date().getTime();
        end_time = end_time.toFixed(2);
        total_time = (end_time - start_time) / 1000;
        total_time = total_time.toFixed(2);
        avarage_time = total_time / total_question;
        avarage_time = avarage_time.toFixed(2);
        accuracy = total_right / total_question * 100;
        accuracy = accuracy.toFixed(2);
        var os = getOs();
        if (os == 'FF' || os == 'SF') { //FireFox、谷歌浏览器用这个
            var text = "正确率: " + accuracy + "%" + "\n" + "总用时: " + total_time + "秒" + "\n" + "平均时间: " + avarage_time + "秒"
        } else {  //IE系列用这个
            var text = "正确率: " + accuracy + "%" + "\r\n" + "总用时: " + total_time + "秒" + "\r\n" + "平均时间: " + avarage_time + "秒"
        }
        $('#accuracy').html(text);
        if (accuracy >= 99 && avarage_time <= 3.5) {
            var result = "恭喜你，通过考核！"
        }
        else {
            var result = "还需要练习，继续加油"
        }
        $('#testresult').html(result);
    }
}


function create_table(data) {
    //第一种：动态创建表格的方式，使用拼接html的方式 （推荐）
    // var html = "";
    // for( var i = 0; i < data.length; i++ ) {
    //     html += "<tr>";
    //     html +=     "<td>" + data[i].name + "</td>"
    //     html +=     "<td>" + data[i].url + "</td>"
    //     html +=     "<td>" + data[i].type + "</td>"
    //     html += "</tr>";
    // }
    // $("#J_TbData").html(html);

    //第二种： 动态创建表格的方式，使用动态创建dom对象的方式
    //清空所有的子节点
    $("#rtable").css({'display': 'block'});
    $("#resulttable").empty();
    //自杀
    // $("#J_TbData").remove();
    console.log($("#resulttable"));
    for (var i = 0; i < data.length; i++) {
        //动态创建一个tr行标签,并且转换成jQuery对象
        var $trTemp = $("<tr></tr>");
        //往行里面追加 td单元格
        $trTemp.append("<td style=\"text-align:center;\">" + data[i].path + "</td>");
        $trTemp.append("<td style=\"text-align: center\">" + data[i].question + "</td>");
        $trTemp.append("<td style=\"text-align: center\">" + data[i].useranswer + "</td>");
        $trTemp.append("<td style=\"text-align: center\">" + data[i].rightanswer + "</td>");
        // $("#J_TbData").append($trTemp);
        $trTemp.appendTo("#resulttable");
    }

}


function Examine() {
    var useranswer = $('input').val();
    var result = Answer(useranswer);
    $('#practicestatus').text('第' + total_question + '/50题');
    if (total_question <= 49) {
        total_question++;
        if (result) {
            total_right++;
        }
        else {
            yanhtml = $(".yanzhengma")[0].src;
            console.log(yanhtml);
            var imgstr = "<img src=" + yanhtml + ">" + "</img>";
            var ua = '';
            useranswer ? ua = useranswer : ua = '空白';
            error_list.push({
                path: imgstr,
                useranswer: ua,
                rightanswer: answer,
                question: question
            })
        }
        GetYanzhengma();  //刷新验证码
        $('input').val("");
        var a = document.getElementsByTagName("input");
        a[0].focus();
    }
    else if (total_question === 50) {
        //结束
        create_table(error_list);
        end_time = new Date().getTime();
        end_time = end_time.toFixed(2);
        total_time = (end_time - start_time) / 1000;
        total_time = total_time.toFixed(2);
        avarage_time = total_time / total_question;
        avarage_time = avarage_time.toFixed(2);
        accuracy = total_right / total_question * 100;
        var os = getOs();
        if (os == 'FF' || os == 'SF') { //FireFox、谷歌浏览器用这个
            var text = "正确率: " + accuracy + "%" + "\n" + "总用时: " + total_time + "秒" + "\n" + "平均时间: " + avarage_time + "秒"
        } else {  //IE系列用这个
            var text = "正确率: " + accuracy + "%" + "\r\n" + "总用时: " + total_time + "秒" + "\r\n" + "平均时间: " + avarage_time + "秒"
        }
        $('#accuracy').html(text);
        if (accuracy >= 99 && avarage_time <= 3.5) {
            var result = "恭喜你，通过考核！"
        }
        else {
            var result = "还需要练习，继续加油"
        }
        $('#testresult').html(result);
    }
}


//设计  bt1 bt2 bt3功能
function gray(btn) {
    btn.css({'background': '#5e5e5e', 'border-color': '#5e5e5e'})
}

function blue(btn) {
    btn.css({'background': '#00aeff', 'border-color': '#00aeff'})
}

$(document).ready(function () {
    $('#bt1').click(function () {
        Mode(0);
    })
})
$(document).ready(function () {
    $('#bt2').click(function () {
        Mode(1);
    })
})

$(document).ready(function () {
    $('#bt3').click(function () {
        Mode(2);
    })
})

//mode control
//mode 0
//mode 1
function Mode(num) {
    error_list = [];

    switch (num) {
        case 0: {
            $("#rtable").css({'display': 'none'});
            $('#userprice').text('验证码随机练习模式');
            $('#practicestatus').text('自由练习');
            blue($('#bt1'));
            gray($('#bt2'));
            gray($('#bt3'));
            GetYanzhengma();  //刷新验证码
            $('input').val("");
            var a = document.getElementsByTagName("input");
            a[0].focus();
        }
            break;
        case 1: {
            $("#rtable").css({'display': 'none'});
            $('#userprice').text('验证码随机测试模式');
            $('#practicestatus').text('第1/10题');
            blue($('#bt2'));
            gray($('#bt1'));
            gray($('#bt3'));
            mode = 1;
            total_right = 0;
            total_question = 0;
            total_time = 0;
            avarage_time = 0;
            start_time = new Date().getTime();
            GetYanzhengma();  //刷新验证码
            $('input').val("");
            var a = document.getElementsByTagName("input");
            a[0].focus();
        }
            break;
        case 2: {
            $("#rtable").css({'display': 'none'});
            $('#userprice').text('验证码随机考核模式');
            $('#practicestatus').text('第1/50题');
            blue($('#bt3'));
            gray($('#bt1'));
            gray($('#bt2'));
            mode = 2;
            total_right = 0;
            total_question = 0;
            total_time = 0;
            avarage_time = 0;
            start_time = new Date().getTime();
            GetYanzhengma();  //刷新验证码
            $('input').val("");
            var a = document.getElementsByTagName("input");
            a[0].focus();
        }
            break;
    }
}


//设置  回车确认  与  E确认
$(document).keydown(function (event) {
    if (event.keyCode == 13 && choice == 1) {
        Control();
    }
    else if (event.keyCode == 69 && choice == 2) {
        Control();
    }

});


//刷新功能
$(document).ready(function () {
    $('.cancel').click(function () {
        Mode(mode);
    })
});


$(document).ready(function () {
    $('.confirm').click(function () {
        Control();
    })
});