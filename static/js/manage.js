$(document).ready(function () {
    function init() {
        if ($("ul>li.active").attr("my_type") == "user") {
            $(".film_area").hide();
            $.ajax(
                {
                    type: 'GET',
                    url: "/get/common_username",
                    success: function (data) {
                        console.log(data);
                        $(".user_table").empty();
                        $(".user_area").show();
                        $(".user_table").append(
                            `<thead>
                                <tr>
                                    <th scope="col">用户名</th>
                                    <th scope="col">操作</th>
                                </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        `
                        )
                        for (let i = 0; i < data.length; i++) {

                            $(".user_table>tbody").append(
                                `
                    <tr>
                        <td>${data[i]}</td>
                        <td >
                            <div class="btn delete badge badge-danger" title="删除">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                    <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>
                                </svg>
                                删除
                            </div>
                        </td>
                    </tr>
                        `
                            )
                        };

                        $(".user_table>tbody").on('click', '.delete', function () {
                            $.ajax({
                                type: 'POST',
                                url: "/delete",
                                data: {
                                    "type": "user",
                                    "username": $(this).parent().prev().text(),
                                },
                                success: (data) => {
                                    console.log(data);
                                    $(this).parent().parent().remove();
                                }
                            });
                        });

                    }
                });
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
                            $(".user_table>tbody").append(
                                `
                        <tr>
                            <td>${$("#register_username").val()}</td>
                            <td >
                                <div class="btn delete badge badge-danger" title="删除">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">
                                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                        <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>
                                    </svg>
                                    删除
                                </div>
                            </td>
                        </tr>
                            `
                            );
                            $("#register").modal('hide');
                        }
                        else {
                            $("#wrong_help").remove();
                            $("#register_button").after(`<small id="wrong_help" class="ml-2" style="color:red">${data["reason"]}</small>`)
                        }
                    },
                });
            });
        }
        else if ($("ul>li.active").attr("my_type") == "film") {
            $(".user_area").hide();
            $.ajax(
                {
                    type: 'GET',
                    url: "/get/film",
                    success: function (data) {
                        console.log(data);
                        $(".film_table").empty();
                        $(".film_area").show();
                        $(".film_table").append(
                            `<thead>
                                <tr>
                                    <th scope="col">电影ID</th>
                                    <th scope="col">电影名称</th>
                                    <th scope="col">操作</th>
                                </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        `
                        )
                        for (let i = 0; i < data.length; i++) {
                            $(".film_table>tbody").append(
                                `
                    <tr>
                        <td>${data[i]["film_id"]}</td>
                        <td>${data[i]["film_name"]}</td>
                        <td >
                            <div class="btn delete p-0 badge badge-danger" title="删除">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                    <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>
                                </svg>
                                删除
                            </div>
                            <a class="text-muted text-decoration-none badge badge-light" title="查看详细" target="_blank" href="http://127.0.0.1:5000/film/introduction?film_id=${data[i]["film_id"]}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle" viewBox="0 0 16 16">
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                    <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                                </svg>
                                详细
                            </a>
                        </td>
                    </tr>
                        `
                            )
                        };
                        $(".delete").click(function () {
                            res = confirm("是否删除电影" + $(this).parent().prev().text() + "?");
                            console.log(res);
                            if (!res) return;
                            $.ajax({
                                type: 'POST',
                                url: "/delete",
                                data: {
                                    "type": "film",
                                    "film_id": $(this).parent().prev().prev().text(),
                                },
                                success: (data) => {
                                    console.log(data);
                                    $(this).parent().parent().remove();
                                }
                            });
                        });
                    }
                });
            $("#add_film_button").click(function () {
                $("#add_film").modal('hide');
                let film_url = $("#film_url").val();
                $("#film_url").val('');
                $.ajax({
                    type: 'POST',
                    url: "/add_film",
                    data: {
                        "film_url": film_url,
                    },
                });
            });

        }
    }
    if (sessionStorage.getItem("current_type")) {
        $("ul>li").removeClass("active");
        $(`ul>li[my_type='${sessionStorage.getItem("current_type")}']`).addClass("active");
    }
    init();
    $("ul>li").click(function () {
        $("ul>li").removeClass("active");
        $(this).addClass("active");
        sessionStorage.setItem("current_type", $(this).attr("my_type"));
        init();
    });
    $("div.quit").click(function () {
        window.location.href = "/admin";
        sessionStorage.clear()
    });
})