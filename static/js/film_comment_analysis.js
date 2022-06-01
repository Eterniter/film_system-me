$(document).ready(function () {
    var myChart_film_user_rating = echarts.init(document.getElementById('film_user_rating'));
    var myChart_film_user_rating_area = echarts.init(document.getElementById('film_user_rating_area'));
    let opts = {
        text: 'loading',
        color: '#c23531',
        textColor: '#fff',
        maskColor: 'rgba(255, 255, 255, 0.2)',
        zlevel: 0,
    }
    myChart_film_user_rating.showLoading(opts);
    myChart_film_user_rating_area.showLoading(opts);
    $.ajax({
        url: "/get/film_comment_analysis?film_id=" + film_id, //请求的服务端地址
        type: "get",
        success: function (ls) {
            console.log(ls);
            let rating_data = ls["rating_data"];
            let area_rating_data = ls["area_rating_data"];
            let film_keywords = ls["film_keywords"];
            WordCloud(document.getElementById('keywords_cloud'),
                {
                    "list": film_keywords,
                    "gridSize": 16,
                    "weightFactor": 30,
                    "color": 'random-dark',
                    "backgroundColor":'transparent',
                    "rotateRatio":0.3
                }
            );
            // for (let i = 0; i < film_keywords.length; i++) {
            //     $("#keywords").append(
            //         `        
            //         <span class="lead">
            //         ${film_keywords[i][0]}
            //         </span>
            //         `
            //     );
            //     if (i == film_keywords.length / 2 - 1) {
            //         $("#keywords").append('<br/>');

            //     }
            // }
            let option = {
                title: {
                    text: '评分数据',
                    subtext: '影评用户对该电影的评分',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{b} : {c}人'
                },
                toolbox: {
                    show: true,
                    feature: {
                        saveAsImage: {}
                    }
                },
                legend: {
                    bottom: 10,
                    left: 'center',
                    data: ['1星', '2星', '3星', '4星', '5星']
                },
                series: [
                    {
                        type: 'pie',
                        roseType: 'area',
                        radius: [10, 150],
                        center: ['50%', '50%'],
                        selectedMode: 'single',
                        data: rating_data,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            };
            myChart_film_user_rating.hideLoading();
            myChart_film_user_rating.setOption(option);

            let series_data = [];
            for (var key in area_rating_data) {
                for (var k in area_rating_data[key]) {
                    if (area_rating_data[key][k] == 0)
                        area_rating_data[key][k] = null;
                }
                series_data.push(
                    {
                        name: key,
                        type: 'bar',
                        stack: "total",
                        barCategoryGap: "30%",
                        label: {
                            show: true,
                            formatter: function (params, ticket, callback) {
                                // console.log(params)
                                val = params.value;
                                if (val < 3)
                                    return '';
                                return params.seriesName + ': ' + val;
                            },
                        },
                        emphasis: {
                            focus: 'series',
                        },
                        data: [
                            area_rating_data[key]["1星"],
                            area_rating_data[key]["2星"],
                            area_rating_data[key]["3星"],
                            area_rating_data[key]["4星"],
                            area_rating_data[key]["5星"],
                        ]
                    },
                );
            }
            option = {
                toolbox: {
                    show: true,
                    feature: {
                        saveAsImage: {}
                    }
                },
                tooltip: {
                    trigger: 'item',
                },
                legend: {
                    bottom: 0,
                    left: 'center'
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    // bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'value'
                },
                yAxis: {
                    type: 'category',
                    data: ['1星', '2星', '3星', '4星', '5星']
                },
                series: series_data
            };
            myChart_film_user_rating_area.hideLoading();
            myChart_film_user_rating_area.setOption(option);

        },
        error: function () {
            console.log("影评分析出错！");
        }
    });

})