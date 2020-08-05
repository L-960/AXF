$(function () {
    $('.confirm').click(function () {
        var $select = $(this);
        var $li = $select.parent();
        var cartid = $li.attr('cartid');
        $.get('/axf/selectcart', {'cartid': cartid}, function (data) {

            if (data['is_select'] === 1) {
                console.log(data['msg']);
                console.log(data['is_select']);
                $select.children('span').children('span').html('√');
            }
            else if (data['is_select'] === 0) {
                console.log(data['msg']);
                console.log(data['is_select']);
                $select.children('span').children('span').html('');
            }
            // console.log(data['msg']);
        })
        console.log(cartid);
    })
})