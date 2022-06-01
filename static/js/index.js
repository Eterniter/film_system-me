$(document).ready(function () {
    $("#custom_recommendation").hide();
    $("#btn_search").click(function () {
        if ($("#input_search").val().length > 0)
            window.location.href = "/search?keyword=" + $("#input_search").val();
    });
    if (sessionStorage.getItem("token")) {
        $.ajax({
            type: 'POST',
            url: "/custom_recommendation",
            data: { "token": sessionStorage.getItem("token") },
            success: function (data) {
                console.log(data)
                if (data["status"] == "error")
                    return;
                data = data["data"]
                if (data.length > 4)
                    col = 2;
                else
                    col = 3;
                for (var i = 0; i < data.length; i++) {
                    item = data[i]
                    $("#custom_recommendation").append(
                        `
        <div class="col-2">
            <a href="/film/introduction?film_id=${item["film_id"]}" class="text-muted text-decoration-none">
                <img src="${item["film_poster"]}" class="img-fluid rounded" alt="${item["film_name"]}">
                <div class="d-flex justify-content-between">
                    <p class="text-truncate ">${item["film_name"]}</p>
                    <p style="color:rgb(255,172,140)">${item["score"]}</p>
                </div>
            </a>
        </div>
        `
                    );
                }
                $("#custom_recommendation").show();
            }
        })
    }
});
