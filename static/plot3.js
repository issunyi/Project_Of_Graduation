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
              text: 'Step Line'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data: ['am_wind_toward', 'pm_wind_toward']
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
                name: 'am_wind_toward',
                type: 'line',
                step: 'start',
                data: data.am_wind_toward
              },
              {
                name: 'pm_wind_toward',
                type: 'line',
                step: 'middle',
                data: data.pm_wind_toward,
              }]
            };
            plot3.setOption(option);
            window.onresize = function() {
	    	    plot3.resize();
	        }
        }
    })
})