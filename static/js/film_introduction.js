$(document).ready(function () {
    $.ajax({
        url: "/get/similarity_film?film_id=" + film_id, //请求的服务端地址
        type: "get",
        success: function (data) {
            console.log(data)
            for (var i = 0; i < data.length; i++) {
                item = data[i]
                $("#similarity_film").append(
                    `
<div class="col-2">
    <a href="/film/introduction?film_id=${item["film_id"]}" class="text-muted text-decoration-none">
        <img src="${item["film_poster"]}" class="img-fluid rounded"
            alt="${item["film_name"]}">
        <p class="text-truncate ">${item["film_name"]}</p>
        <span class="score">${item["score"]}</span>
    </a>
</div>`
                )
            }
        },
        error: function () {
            ; //错误的处理
        }
    });

    if (sessionStorage.getItem('token')) {
        $.ajax({
            type: 'POST',
            url: "/record",
            data: {
                "token": sessionStorage.getItem("token"),
                "film_id": film_id
            },
            success: function (data) {
                console.log(data);
            },
        });
    }
})