$(document).ready(function(){
    // TODO: 对于发布房源，只有认证后的用户才可以，所以先判断用户的实名认证状态
    $.get('/api/1.0/users/auth', function (response) {
        if (response.errno == '0') {
             // TODO: 如果用户已实名认证,那么就去请求之前发布的房源
            $.get('/api/1.0/users/houses', function (response) {
                 if (response.errno == '0') {
                     var housesList_html = template('houses-list-tmpl', {'houses': response.data.houses});
                     $('#houses-list').html(housesList_html);
                } else {
                    alert(response.errmsg);
                }
            })
        } else if (response.errno == '4101') {
            location.href = '/login.html';
        } else {
            $(".auth-warn").show();

        }
    });
});
