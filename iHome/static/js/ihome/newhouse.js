function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get('/api/1.0/areas', function (response) {
        if (response.errno == '0') {
            var area_html = template('areas-tmpl', {'areas': response.data});
            $('#area-id').html(area_html);
            $('#form-house-info').show();
            $('#form-house-image').hide();
        } else{
            alert(response.errmsg);
        }
    });
    // TODO: 处理房屋基本信息提交的表单数据
    $('#form-house-info').submit(function (event) {
        event.preventDefault();
        // 收集表单数据
        var params = {};
        $(this).serializeArray().map(function (obj) {
            // console.log(obj);
            params[obj.name] = obj.value;
        });
        var facility = [];
        $(':checkbox:checked[name=facility]').each(function (i, elem) {
            // console.log(elem);
            facility[i] = elem.value;
        });
        params['facility'] = facility;
        $.ajax({
            url: '/api/1.0/houses',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify(params),
            headers: {'X-CSRFToken': getCookie('csrf_token')},
            success: function (response) {
                if (response.errno == '0') {
                    $('#form-house-info').hide();
                    $('#house-id').val(response.data.house_id);
                    $('#form-house-image').show();
                } else {
                    alert(response.errmsg);
                }
            }
        })
    });
    // TODO: 处理图片表单的数据
    $('#form-house-image').submit(function (event) {
        event.preventDefault();
        $(this).ajaxSubmit({
            url: '/api/1.0/houses/'+$('#house-id').val()+'/images',
            type: 'post',
            headers: {'X-CSRFToken': getCookie('csrf_token')},
            success: function (response) {
                if (response.errno == '0') {
                    $('.house-image-cons').html('<image src="'+response.data.url+'">')
                } else {
                    alert(response.errmsg)
                }
            }
        })
    })
});