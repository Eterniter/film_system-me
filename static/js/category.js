$(document).ready(function () {


    $("#film_type li").click(function () {

        $("#film_type li").removeClass("list-active");
        $(this).addClass("list-active");
        var film_type = $("#film_type .list-inline-item.list-active").text();
        var film_producer = $("#film_producer .list-inline-item.list-active").text();
        window.location.href = `/category?film_type=${film_type}&film_producer=${film_producer}&current_page=1`
    })
    $("#film_producer li").click(function () {

        $("#film_producer li").removeClass("list-active");
        $(this).addClass("list-active");
        var film_type = $("#film_type .list-inline-item.list-active").text();
        var film_producer = $("#film_producer .list-inline-item.list-active").text();
        window.location.href = `/category?film_type=${film_type}&film_producer=${film_producer}&current_page=1`
    })
    console.log(data);
    $("#film_type li").each(function () {
        if ($(this).text() == current_film_type)
            $(this).addClass("list-active");
    })
    $("#film_producer li").each(function () {
        if ($(this).text() == current_film_producer)
            $(this).addClass("list-active");
    })
    for (var i = 0; i < data.length; i++) {
        item = data[i]
        $("#showcase").append(
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
    if (data.length <= 0) {
        $(".d-none").removeClass('d-none');
        $("#Pagination").remove()
    } else {
        if (page_num > 1) {
            $("#Pagination ul").append(
                `
<li class="page-item">
    <a class="page-link" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
    </a>
</li>
`);
            for (var i = 1; i <= page_num; i++)
                if (i == current_page)
                    $("#Pagination ul").append(`
<li class="page-item active"><a class="page-link">${i}</a></li>
`);
                else $("#Pagination ul").append(`
<li class="page-item"><a class="page-link">${i}</a></li>
`);

            $("#Pagination ul").append(
                `
<li class="page-item">
    <a class="page-link" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
    </a>
</li>
`);
            if (current_page == 1)
                $("a[aria-label='Previous']").addClass("d-none");
            if (current_page == page_num)
                $("a[aria-label='Next']").addClass("d-none");
            $("li.page-item a.page-link").click(function () {
                console.log($(this));
                var film_type = $("#film_type .list-inline-item.list-active").text();
                var film_producer = $("#film_producer .list-inline-item.list-active").text();
                var index = Number($(this).text());
                if (isNaN(index)) {
                    var current_index = Number($("li.page-item.active").text());//此处.active对应的是分页的样式，无错
                    if ($(this).attr("aria-label") == "Next")
                        window.location.href = `/category?film_type=${film_type}&film_producer=${film_producer}&current_page=${current_index + 1}`
                    else
                        window.location.href = `/category?film_type=${film_type}&film_producer=${film_producer}&current_page=${current_index - 1}`
                }
                else
                    window.location.href = `/category?film_type=${film_type}&film_producer=${film_producer}&current_page=${index}`
            })
        }
        else {
            $("#Pagination").remove()
        }
    }

    console.log("done")
})
