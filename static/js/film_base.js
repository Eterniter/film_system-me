$(document).ready(function () {
    // for (var i = 0; i < $(".card-body a").length; i++)
    //     if ($(".card-body a")[i].href == window.location.href)
    //         $($(".card-body a")[i]).addClass("active")
    var url=window.location.href.split('/')
    url=url[url.length-1];
    $(".card-body a[href$='"+url+"']").addClass("active");
})

