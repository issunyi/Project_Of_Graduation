layui.use(['echarts'], function() {
     $.ajax({
         url: '/get_environment_data',
         type: 'GET',
         dataType: 'json',
         success: function (data) {
             let echarts = layui.echarts;
             var plot1_total_power = echarts.init(document.getElementById('plot1_total_power'), null, {
                 width: 1000,
                 height: 400
             });
             let base = +new Date(1988, 9, 3);
             let oneDay = 24 * 3600 * 1000;
             option = {
                 tooltip: {trigger: 'axis', position: function (pt) {
                     return [pt[0], '10%'];
                 }
                 },
                 title: {text: '系统负载总功率'
                 },
                 toolbox: {feature: {
                     dataZoom: {yAxisIndex: 'none'
                     }, restore: {}, saveAsImage: {}
                 }
                 },
                 xAxis: {type: 'category', boundaryGap: false,
                     data: data.date_time
                 },
                 yAxis: {type: 'value', boundaryGap: [0, '100%']
                 },
                 dataZoom: [{
                     type: 'inside',
                     start: 0,
                     end: 20
                 }, {
                     start: 0,
                     end: 20
                 }
                 ],
                 series: [{
                     name: '系统负载总功率',
                     type: 'line',
                     smooth: true,
                     symbol: 'none',
                     areaStyle: {},
                     data: data.total_active_power
                 }
                 ]
             };
             plot1_total_power.setOption(option);
	         window.onresize = function() {
	    	    plot1_total_power.resize();
	        }
         }
     })
})