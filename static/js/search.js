$(document).ready(function () {
    data = JSON.parse(data_json);
    console.log(data)
    $("#showcase").append(`<div class="col-12">本次搜索的结果有${data.length}条</div>`);
    if (data.length > 4)
        col = 2;
    else
        col = 3;
    for (var i = 0; i < data.length; i++) {
        item = data[i]
        $("#showcase").append(
`
<div class="col-${col}">
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

});
