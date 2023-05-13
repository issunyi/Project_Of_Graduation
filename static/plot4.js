layui.use(['echarts'], function() {
    $.ajax({
        url: '/get_environment_data',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let echarts = layui.echarts;
            var plot4 = echarts.init(document.getElementById('plot4'), null, {
                width: 800,
                height: 400
            });
            option = {
            title: {
              text: 'Step Line'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data: ['weather_1', 'weather_2']
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
              data: data.date_time
            },
            yAxis: {
              type: 'value'
            },
            series: [
              {
                name: 'weather_1',
                type: 'line',
                step: 'start',
                data: data.weather_1
              },
              {
                name: 'weather_2',
                type: 'line',
                step: 'middle',
                data: data.weather_2,
              }]
            };
            plot4.setOption(option);
            window.onresize = function() {
		        plot4.resize();
	        }
        }
    })
})