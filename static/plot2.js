layui.use(['echarts'], function() {
    $.ajax({
        url: '/get_environment_data',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let echarts = layui.echarts;
            var plot2 = echarts.init(document.getElementById('plot2'), null, {
                width: 800,
                height: 400
            });
            option = {
            // Make gradient line here
            visualMap: [
              {
                show: false,
                type: 'continuous',
                min: 0,
                max: 400
              }, {
                show: false,
                type: 'continuous',
                seriesIndex: 1,
                dimension: 0,
                min: 0,
                max: data.date_time.length - 1
                }
            ],
            title: [
              {
                left: 'center',
                text: '环境最高温度'
              }, {
                top: '55%',
                left: 'center',
                  text: '环境最低温度'
                }
            ],
            tooltip: {
              trigger: 'axis'
            },
            xAxis: [
              {
                  type: 'category',
                  data: data.date_time,
              },
                {
                    type: 'category',
                    data: data.date_time,
                    gridIndex: 1
            }
            ],
            yAxis: [
              {},
                {
                gridIndex: 1
            }
            ],
            toolbox: {
              feature: {
                saveAsImage: {}
              }
            },
            grid: [
              {
                bottom: '60%'
              },
              {
                top: '60%'
              }
            ],
            series: [
              {
                type: 'line',
                showSymbol: true,
                name: '最高温度',
                data: data.highest_temp
              },
                    {
                type: 'line',
                showSymbol: true,
                name: '最低温度',
                data: data.lowest_temp,
                xAxisIndex: 1,
                yAxisIndex: 1
                }
            ]
            };
             plot2.setOption(option);
	         window.onresize = function() {
	    	    plot2.resize();
	        }
        }
    })
})

