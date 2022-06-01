$(document).ready(function () {
    var myChart_film_user_residence = echarts.init(document.getElementById('film_user_residence'));
    var myChart_film_user_register_time = echarts.init(document.getElementById('film_user_register_time'));
    let opts = {
        text: 'loading',
        color: '#c23531',
        textColor: '#fff',
        maskColor: 'rgba(255, 255, 255, 0.2)',
        zlevel: 0,
    }
    myChart_film_user_residence.showLoading(opts);
    myChart_film_user_register_time.showLoading(opts);
    $.ajax({
        url: "/get/film_user_analysis?film_id=" + film_id, //请求的服务端地址
        type: "get",
        success: function (ls) {
            // console.log(ls);
            // ls['residence']={"湖北": 3, "广东": 5, "北京": 28, "湖南": 1, "江西": 1}
            let dataList = [];
            let sum_num = 0;
            for (let key in ls["residence"]) {
                dataList.push({ name: key, value: ls["residence"][key] });
                sum_num += ls["residence"][key];
            }
            dataList = dataList.sort((a, b) => b.value - a.value);
            for (let i = 0; i < dataList.length; i++) {
                $("#film_user_residence_table").append("<tr><td>"
                    + dataList[i].name + "</td>" + "<td>" + dataList[i].value
                    + "</td>" + "<td>" + (dataList[i].value / sum_num).toFixed(2) + "</td></tr>")
            }

            let option = {
                title: {
                    text: "用户常居住地分布",
                    textStyle: {
                        fontFamily: "Arial",
                        fontWeight: "lighter"
                    }
                },
                toolbox: {
                    show: true,
                    feature: {
                        saveAsImage: {}
                    }
                },
                tooltip: {
                    formatter: function (params, ticket, callback) {
                        val = params.value
                        if (isNaN(val))
                            val = 0;
                        return params.seriesName + '<br/>' + params.name + ': ' + val;
                    }//数据格式化
                },
                visualMap: {
                    min: 0,
                    max: dataList[0].value,
                    left: 'left',
                    top: 'bottom',
                    text: ['多', '少'],//取值范围的文字
                    inRange: {
                        color: ['#e0ffff', '#006edd']//取值范围的颜色
                    },
                    show: true,//图注
                    calculable: true
                },
                geo: {
                    map: 'china',
                    roam: false,//不开启缩放和平移
                    zoom: 1.3,//视角缩放比例
                    label: {
                        normal: {
                            show: true,
                            fontSize: '10',
                            color: 'rgba(0,0,0,0.7)'
                        }
                    },
                    itemStyle: {
                        normal: {
                            borderColor: 'rgba(0, 0, 0, 0.2)'
                        },
                        emphasis: {
                            areaColor: '#F3B329',//鼠标选择区域颜色
                            shadowOffsetX: 0,
                            shadowOffsetY: 0,
                            shadowBlur: 20,
                            borderWidth: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                },
                series: [
                    {
                        name: '用户居住人数',
                        type: 'map',
                        geoIndex: 0,
                        data: dataList
                    }
                ]
            };
            myChart_film_user_residence.hideLoading();
            myChart_film_user_residence.setOption(option);
            myChart_film_user_residence.on('click', function (params) {
                console.log(params);
                val = params.value
                if (isNaN(val))
                    val = 0;
                alert(params.name + ': ' + val);
            });


            var x_data = [];
            var y_data = [];
            for (var key in ls["register_time"]) {
                x_data.push(key);
                y_data.push(ls["register_time"][key])
            }
            option = {
                title: {
                    text: "用户加入时间",
                    textStyle: {
                        fontFamily: "Arial",
                        fontWeight: "lighter"
                    }
                },
                toolbox: {
                    show: true,
                    feature: {
                        saveAsImage: {}
                    }
                },
                tooltip: {
                    formatter: function (params, ticket, callback) {
                        val = params.value
                        if (isNaN(val))
                            val = 0;
                        return params.seriesName + '<br/>' + params.name + ': ' + val;
                    }//数据格式化
                },
                xAxis: {
                    data: x_data
                },
                yAxis: {},
                series: [
                    {
                        data: y_data,
                        type: 'line',
                        smooth: true,
                        name: "人数"
                    }
                ]
            };
            myChart_film_user_register_time.hideLoading();
            myChart_film_user_register_time.setOption(option);
        },
        error: function () {
            console.log("影评用户分析出错！");
        }
    });

})