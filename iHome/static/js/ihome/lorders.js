//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    // TODO: 查询房东的订单
    $.get('/api/1.0/orders?role=landlord', function (response) {
        if (response.errno == '0') {
            var orders_list_html = template('orders-list-tmpl', {'orders': response.data.orders});
            $('.orders-list').html(orders_list_html);
            // TODO: 查询成功之后需要设置接单和拒单的处理
            $(".order-accept").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-accept").attr("order-id", orderId);
            });
            $(".order-reject").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);
            });
            function order_action(order_buton, action) {
                var orderId = order_buton.attr("order-id");
                var reason = '';
                if (action == 'reject') {
                    reason = $('#reject-reason').val();
                }
                var params = {
                    'reason': reason,
                    'action': action
                };
                $.ajax({
                    url: '/api/1.0/orders/'+orderId+'/status',
                    type: 'put',
                    contentType: 'application/json',
                    data: JSON.stringify(params),
                    headers: {'X-CSRFToken': getCookie('csrf_token')},
                    success: function (response) {
                        if (response.errno == '0') {
                            $('.orders-list>li[order-id='+orderId+'] .order-operate').hide();
                            if (action == 'accept') {
                                $('#accept-modal').modal('hide');  // 手动关模态框
                                $('.orders-list>li[order-id='+orderId+'] .order-text li>span').html('待评价');
                            }else {
                                $('#reject-modal').modal('hide');
                                $('.orders-list>li[order-id='+orderId+'] .order-text li>span').html('已拒单');
                            }
                        } else {
                            alert(response.errmsg);
                        }
                    }
                });
            }
            $('.modal-accept').on('click', function () {
                order_action($(this), 'accept');
            });
            $('.modal-reject').on('click', function () {
                order_action($(this), 'reject');
            });
        }else if (response.errno == '4101'){
            location.href = '/login.html';
        }else {
            alert(response.errmsg);
        }
    });
});
