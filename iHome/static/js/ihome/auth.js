function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // TODO: 查询用户的实名认证信息
    $.get('/api/1.0/users/auth', function (response) {
        if (response.errno == '0') {
            if (response.data.real_name && response.data.id_card) {
                $('#real-name').val(response.data.real_name).disabled();
                $('#id-card').val(response.data.id_card).disabled();
                $(':submit').hide();
            }
        }else if (response.errno == '4101') {
            $('.error-msg').text(response.errmsg);
            location.href = '/';
        }else {
            $('.error-msg').text(response.errmsg);
        }
    });

    // TODO: 管理实名信息表单的提交行为
    $('#form-auth').submit(function (event) {
        event.preventDefault();
        var real_name = $('#real-name').val();
        var id_card = $('#id-card').val();
        var params = {
            'real_name': real_name,
            'id_card': id_card
        };
        $.ajax({
            url: '/api/1.0/users/auth',
            type: 'post',
            dataType: 'application/json',
            data: JSON.stringify(params),
            headers: {'X-CSRFToken': getCookie('csrf_token')},
            success: function (response) {
                if (resonse.errno == '0') {
                    showSuccessMs();
                    $('#real-name').val(response.data.real_name).disabled();
                    $('#id-card').val(response.data.id_card).disabled();
                    $(':submit').hide();
                }else {
                    $('.error-msg').text(response.errmsg);
                }
            }
        });
    });
});