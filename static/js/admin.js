$(document).ready(function () {
    $("#login_button").click(function () {
        $.ajax({
            type: 'POST',
            url: "/login",
            data: {
                username: $("#login_username").val(),
                password: $("#login_password").val(),
                authority: "admin"
            },
            success: function (data) {
                console.log(data);
                if (data["status"] == "success") {
                    // sessionStorage.setItem("token", data["token"]);
                    // sessionStorage.setItem("username", data["username"]);
                    window.location.href = "/manage";
                }
                else {
                    $("#wrong_help").remove();
                    $("#login_button").after(`<small id="wrong_help" class="ml-2" style="color:red">${data["reason"]}</small>`)
                }
            },
        });
    });
})