$(document).ready(function () {
    if (sessionStorage.getItem("token")) {
        $("button[data-target='#login']").hide();
        $("button[data-target='#register']").hide();
        $("div.navbar-nav.mr-auto").after(
            `
        <div id="welcome" class="dropdown">
            <button class="btn dropdown-toggle" type="button" data-toggle="dropdown">
            欢迎您,${sessionStorage.getItem("username")}
            </button>
            <div class="dropdown-menu">
                <a class="dropdown-item" href="/history">浏览历史</a>
                <div class="dropdown-item logout">退出登录</div>
            </div>
        </div>
        `
        );
        $(".logout").click(function () {
            sessionStorage.removeItem("token");
            sessionStorage.removeItem("username");
            $("button[data-target='#login']").show();
            $("button[data-target='#register']").show();
            $("#welcome").remove();
            $("#custom_recommendation").hide();
            let url = window.location.href;
            url = url.split('/');
            if (url[url.length - 1] == "history")
                window.location.href = '/index';
        });
    }
    $("#register_button").click(function () {
        $.ajax({
            type: 'POST',
            url: "/register",
            data: {
                username: $("#register_username").val(),
                password: $("#register_password").val(),
            },
            success: function (data) {
                console.log(data);
                if (data["status"] == "success") {
                    sessionStorage.setItem("token", data["token"]);
                    sessionStorage.setItem("username", data["username"]);
                    location.reload();
                }
                else {
                    $("#wrong_help").remove();
                    $("#register_button").after(`<small id="wrong_help" class="ml-2" style="color:red">${data["reason"]}</small>`)
                }
            },
        });
    });
    $("#login_button").click(function () {
        $.ajax({
            type: 'POST',
            url: "/login",
            data: {
                username: $("#login_username").val(),
                password: $("#login_password").val(),
            },
            success: function (data) {
                console.log(data);
                if (data["status"] == "success") {
                    sessionStorage.setItem("token", data["token"]);
                    sessionStorage.setItem("username", data["username"]);
                    location.reload();
                }
                else {
                    $("#wrong_help").remove();
                    $("#login_button").after(`<small id="wrong_help" class="ml-2" style="color:red">${data["reason"]}</small>`)
                }
            },
        });
    });
})
