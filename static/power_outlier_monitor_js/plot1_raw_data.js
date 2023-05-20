layui.use(['echarts'], function() {
    $.ajax({
        url: '/get_threshold_data',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let echarts = layui.echarts;
            var plot1_raw_data = echarts.init(document.getElementById('plot1_raw_data'), null, {
                width: 800,
                height: 400
            });

            option = {
            title: {
              text: '系统负载功率'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data: ['白天风力风向', '夜晚风力风向']
            },
            grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
            },
            toolbox: {
              feature: {
                saveAsImage: {}
              }
            },
            xAxis: {
              type: 'category',
              data: data.raw_x
            },
            yAxis: {
              type: 'value'
            },
            series: [{
                name: '白天风力风向',
                type: 'line',
                step: 'start',
                data: data.raw_y,
                showSymbol: true
            }]
            };

            plot1_raw_data.setOption(option);
	        window.onresize = function() {
            plot1_raw_data.resize();
        }


        }

    })
})