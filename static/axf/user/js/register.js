$(function () {
    var $username = $("#username_input");
    $username.change(function () {
        var username = $username.val().trim();
        if (username.length) {
            // 将用户名发给服务器进行校验
            $.getJSON('/axf/check_user/', {'username': username}, function (data) {
                // console.log(data);
                var $username_info = $("#username_info");
                if (data['status'] === 200) {
                    $username_info.html('用户名可用').css("color", 'green');
                    // console.log($username_info.css("color"));
                } else if (data['status'] === 901) {
                    $username_info.html('用户名不可用').css("color", 'red')
                }
            })
        }
    })
})

$(function () {

    var $password_input = $("#password_input");
    var $password_confirm_input = $("#password_confirm_input");

    $password_confirm_input.change(function () {
        var $password_info = $("#password_info");
        if ($password_input.val() == $password_confirm_input.val()) {
            $password_info.html("密码一致").css("color", "green");

        } else {
            $password_info.html("两次输入密码不一致").css("color", "red");
        }

    })

})

function check() {
    var $username = $("#username_input");
    var username = $username.val().trim();
    if (!username) {
        return false
    }

    var username_info_color = $("#username_info").css("color");
    if (username_info_color != 'rgb(0, 128, 0)') {
        return false
    }

    var password_info_color = $("#password_info").css("color");
    if (password_info_color != 'rgb(0, 128, 0)') {
        return false
    }

    var $password_input = $("#password_input");
    var password = $password_input.val().trim();
    $password_input.val(md5(password));

    var $password_confirm_input = $("#password_confirm_input");
    var password_confirm = $password_confirm_input.val().trim();
    $password_input.val(md5(password_confirm));

    return true
}