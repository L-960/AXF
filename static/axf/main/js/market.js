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
})