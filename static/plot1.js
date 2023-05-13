layui.use(['echarts'], function() {
     $.ajax({
         url: '/get_environment_data',
         type: 'GET',
         dataType: 'json',
         success: function (data) {
             let echarts = layui.echarts;
             var plot1 = echarts.init(document.getElementById('plot1'), null, {
                 width: 800,
                 height: 400
             });
             let base = +new Date(1988, 9, 3);
             let oneDay = 24 * 3600 * 1000;

             option = {
                 tooltip: {trigger: 'axis', position: function (pt) {
                     return [pt[0], '10%'];
                 }
                 },
                 title: {left: 'center', text: 'Large Ara Chart'
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
                     name: 'Fake Data',
                     type: 'line',
                     smooth: true,
                     symbol: 'none',
                     areaStyle: {},
                     data: data.total_active_power
                 }
                 ]
             };
             plot1.setOption(option);
	         window.onresize = function() {
	    	    plot1.resize();
	        }
         }
     })
})