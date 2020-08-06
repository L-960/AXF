$(function () {
    $("#all_types").click(function () {
        var $all_type_container = $("#all_type_container");
        $all_type_container.slideDown();
        var $all_type = $(this);
        var $span =$all_type.find("span").find("span")
        $span.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up")

        var $sort_rule_container = $("#sort_rule_container");
        $sort_rule_container.slideUp();
        var $sort_rule = $("#sort_rule");
        var $span_sort_rule = $sort_rule.find("span").find("span");
        $span_sort_rule.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down")
    })

    $("#all_type_container").click(function () {
        var $all_type_container = $(this);
        $all_type_container.slideUp();

        var $all_type = $("#all_types");
        var $span =$all_type.find("span").find("span")
        $span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down")
    })



    $("#sort_rule").click(function () {
        var $sort_rule_container = $("#sort_rule_container")
        $sort_rule_container.slideDown();

        var $sort_rule = $(this);
        var $span = $sort_rule.find("span").find("span");
        $span.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");

        var $all_type_container = $("#all_type_container");
        $all_type_container.slideUp();

        var $all_type = $("#all_types");
        var $span_all_type =$all_type.find("span").find("span")
        $span_all_type.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down")
    })

    $("#sort_rule_container").click(function () {
        var $sort_rule_container = $(this);
        $sort_rule_container.slideUp();

        var $sort_rule = $("#sort_rule");
        var $span = $sort_rule.find("span").find("span");
        $span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down")
    })

    $(".subShopping").click(function () {
        console.log('sub');
        var $add = $(this);
        var goodsid = $add.attr("goodsid");
        $.get('/axf/subtocart',{'goodsid':goodsid}, function (data) {
            //中间件检测到未登陆 就跳转登陆
            if (data['status'] === 301 ){
                window.open('/axf/login/', target="_self");
            }else if(data['status'] === 200){
                // 找下一个兄弟节点
                $add.next('span').html(data['c_goods_num'])
            }else if(data['status'] === 302){
                // 找下一个兄弟节点
                $add.next('span').html(data['c_goods_num'])
            }
            // // console.log(data);
        })
    })

    $(".addShopping").click(function () {
        console.log('add');
        var $add = $(this);
        var goodsid = $add.attr("goodsid");

        $.get('/axf/addtocart',{'goodsid':goodsid}, function (data) {
            //中间件检测到未登陆 就跳转登陆
            if (data['status'] === 301 ){
                window.open('/axf/login/', target="_self");
            }else if(data['status'] === 200){
                // 找兄弟节点
                $add.prev('span').html(data['c_goods_num'])
            }
            // // console.log(data);
        })

    })

})

