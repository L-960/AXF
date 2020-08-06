$(function () {

    $(".confirm").click(function () {

        console.log("change state");

        var $confirm = $(this);

        var $li = $confirm.parents("li");

        var cartid = $li.attr('cartid');

        $.getJSON("/axf/changecartstate/", {'cartid': cartid}, function (data) {
            console.log(data);

            if (data['status'] === 200) {
                $("#total_price").html(data['total_price']);
                if (data['c_is_select']) {
                    $confirm.find("span").find("span").html("√");
                } else {
                    $confirm.find("span").find("span").html("");
                }
                if (data['is_all_select']) {
                    $(".all_select span span").html("√");
                } else {
                    $(".all_select span span").html("");

                }
            }

        })

    })

    // 购物车减商品
    $(".subShopping").click(function () {

        var $sub = $(this);

        var $li = $sub.parents("li");

        var cartid = $li.attr("cartid");

        $.getJSON("/axf/subshopping/", {"cartid": cartid}, function (data) {
            console.log(data);

            if (data['status'] === 200) {
                // $("#total_price").html(data['total_price']);
                $("#total_price").html(data['total_price']);
                if (data['c_goods_num'] > 0) {
                    var $span = $sub.next("span");
                    $span.html(data['c_goods_num']);
                } else {
                    $li.remove();
                }
            }

        })

    })

    // 购物车加商品
    $(".addShopping").click(function () {

        var $sub = $(this);

        var $li = $sub.parents("li");
        //获取商品id
        var cartid = $li.attr("cartid");

        $.getJSON("/axf/addshopping/", {"cartid": cartid}, function (data) {
            console.log(data);
            if (data['status'] === 200) {
                $("#total_price").html(data['total_price']);
                var $span = $sub.prev("span");
                $span.html(data['c_goods_num']);

            }

        })

    })


    $(".all_select").click(function () {

        var $all_select = $(this);

        var select_list = [];

        var unselect_list = [];

        //遍历
        $(".confirm").each(function () {

            var $confirm = $(this);

            var cartid = $confirm.parents("li").attr("cartid");

            if ($confirm.find("span").find("span").html().trim()) {
                //相当于append
                select_list.push(cartid);
            } else {
                unselect_list.push(cartid);
            }

        })

        if (unselect_list.length > 0) {
            $.getJSON("/axf/allselect/", {"cart_list": unselect_list.join("#")}, function (data) {
                console.log(data);
                if (data['status'] === 200) {
                    $(".confirm").find("span").find("span").html('√');
                    $all_select.find("span").find("span").html("√");
                    $("#total_price").html(data['total_price']);
                }
            })
        } else {
            if (select_list.length > 0) {
                //不能传[] join
                $.getJSON("/axf/allselect/", {"cart_list": select_list.join("#")}, function (data) {
                    console.log(data);
                    if (data['status'] === 200) {
                        $(".confirm").find("span").find("span").html('');
                        $all_select.find("span").find("span").html("");
                        $("#total_price").html(data['total_price']);
                    }
                })
            }

        }


    })

    //生成订单 打开新页面
    $("#make_order").click(function () {

        var select_list = [];

        var unselect_list = [];
        // 循环
        $(".confirm").each(function () {

            var $confirm = $(this);

            var cartid = $confirm.parents("li").attr("cartid");

            if ($confirm.find("span").find("span").html().trim()) {
                select_list.push(cartid);
            } else {
                unselect_list.push(cartid);
            }

        })

        if (select_list.length === 0) {
            return
        }

        $.getJSON("/axf/makeorder/", function (data) {
            console.log(data);

            if (data['status'] === 200) {
                window.open('/axf/orderdetail/?orderid=' + data['order_id'], target = "_self");
            }

        })
    })


})