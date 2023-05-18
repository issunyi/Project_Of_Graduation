layui.use(['echarts'], function() {
    $.ajax({
        url: '/get_environment_data',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let echarts = layui.echarts;
            var plot3 = echarts.init(document.getElementById('plot3'), null, {
                width: 800,
                height: 400
            });
            option = {
            title: {
              text: '风力风向'
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
              data: data.date_time
            },
            yAxis: {
              type: 'value'
            },
            series: [
              {
                name: '白天风力风向',
                type: 'line',
                step: 'start',
                data: data.am_wind_toward,
                showSymbol: true,
              },
              {
                name: '夜晚风力风向',
                type: 'line',
                step: 'middle',
                data: data.pm_wind_toward,
                showSymbol: true,
              }]
            };
            plot3.setOption(option);
            window.onresize = function() {
	    	    plot3.resize();
	        }
        }
    })
})