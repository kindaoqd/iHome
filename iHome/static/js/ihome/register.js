function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}
var imageCodeId = "";
// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    var uuid = generateUUID();
    // 拼接url字符串，传递参数uuid,lastuuid
    var image_code_url = '/api/1.0/verify_code?uuid=' + uuid + '&last_uuid=' + imageCodeId;

    $('.image-code>img').attr('src', image_code_url);
    // 设置后记录uuid，作为前次记录
    imageCodeId = uuid;
}

function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    // 通过ajax方式向后端接口发送请求，让后端发送短信验证码
    var params = {
        'uuid': imageCodeId,
        'mobile': mobile,
        'verify_code': imageCode
    };
    $.ajax({
        url: '/api/1.0/sms_code',
        type: 'post',
        contentType: 'application/json',
        data:JSON.stringify(params),
        headers: {'X-CSRFToken': getCookie('csrf_token')},
        success: function (response) {
            if (response.errno == '0') {
                 $("#phone-code-err span").html('发送成功，请注意查收并输入验证码');
                $("#phone-code-err").show();
                var num = 30;
                var t = setInterval(function () {
                    if (num == 0) {
                        clearInterval(t);
                        $(".phonecode-a").attr("onclick", "sendSMSCode();").html('重新发送');
                    } else {
                        $(".phonecode-a").html(num+'秒');
                        num--;
                    }
                }, 1000)
            } else {
                $("#phone-code-err span").html(response.errmsg);
                $("#phone-code-err").show();
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
                generateImageCode();
            }
        }
    })
}

$(document).ready(function() {
    generateImageCode();  // 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });

    // TODO: 注册的提交(判断参数是否为空)
})
