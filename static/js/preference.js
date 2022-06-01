$(document).ready(function () {
    let area_ls = ["浙江", "北京", "江苏", "四川", "香港", "上海", "山东", "陕西", "福建",
        "海南", "天津", "广东", "湖南", "辽宁", "湖北", "重庆", "安徽", "内蒙古", "云南", "西藏", "吉林",
        "台湾", "河北", "河南", "黑龙江", "江西", "山西", "贵州", "新疆", "广西", "澳门", "宁夏", "甘肃", "青海"];
    for (let i = 0; i < area_ls.length; i++) {
        $("#select_area").append(`<option value="${area_ls[i]}">${area_ls[i]}</option>`);
    }
    let opts = {
        text: 'loading',
        color: '#c23531',
        textColor: '#fff',
        maskColor: 'rgba(255, 255, 255, 0.2)',
        zlevel: 0,
    }
    function randomColor() {
        let col = "#";
        for (let i = 0; i < 6; i++) col += parseInt(Math.random() * 16).toString(16);
        return col;
    }
    function debounce(fn, delay = 200) {
        // 定时器，用来 setTimeout
        var timer
        // 返回一个函数，这个函数会在一个时间区间结束后的 delay 毫秒时执行 fn 函数
        return function () {
            // 保存函数调用时的上下文和参数，传递给 fn
            var context = this
            var args = arguments
            // 每次这个返回的函数被调用，就清除定时器，以保证不执行 fn
            clearTimeout(timer)
            // 当返回的函数被最后一次调用后（也就是用户停止了某个连续的操作），
            // 再过 delay 毫秒就执行 fn
            timer = setTimeout(function () {
                fn.apply(context, args)
            }, delay)
        }
    }
    function area_change() {
        console.log($('#select_area').val())
        $(".lead").text(`${$('#select_area').val()}地区偏好的电影`)
        $.ajax(
            {
                type: 'GET',
                url: "/get/preference",
                data: {
                    "area_name": $('#select_area').val(),
                },
                success: function (data) {
                    console.log(data);
                    if (JSON.stringify(data["film_type"]) == '{}')
                        console.log(666);
                    film_type = data["film_type"];
                    data = data["favor_films"];
                    if (data.length > 12)
                        data = data.slice(0, 12);
                    $("#preference_film").empty();
                    for (var i = 0; i < data.length; i++) {
                        item = data[i]
                        $("#preference_film").append(
                            `
                <div class="col-3">
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
                    };
                    $("#preference_film>div.col-3").addClass("element_add")
                    // $('#preference_film>div.col-3').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
                    // });
                    film_type_keys = Object.keys(film_type).sort(function (a, b) { return film_type[a] - film_type[b] });
                    series_data = []
                    for (var k in film_type_keys) {
                        // console.log(film_type_keys[k],film_type[film_type_keys[k]])
                        series_data.push({
                            value: film_type[film_type_keys[k]],
                            itemStyle: {
                                color: randomColor()
                            }
                        })
                    }
                    let option = {
                        tooltip: {
                            trigger: 'item',
                            formatter: '{b}:{c}'
                        },
                        xAxis: {
                            type: 'category',
                            data: film_type_keys
                        },
                        yAxis: {
                            type: 'value'
                        },
                        label: {
                            show: true
                        },
                        emphasis: {
                            focus: 'items',
                        },
                        series: [
                            {
                                data: series_data,
                                type: 'bar'
                            }
                        ]
                    };
                    myChart_film_type.hideLoading();
                    myChart_film_type.setOption(option);
                },
            }
        )
    }
    var myChart_film_type = echarts.init(document.getElementById('film_type'));
    myChart_film_type.showLoading(opts);

    area_change();
    $("#select_area").change(debounce(area_change));
})