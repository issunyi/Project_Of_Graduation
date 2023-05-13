layui.use(['echarts'], function() {
     $.ajax({
         url: '/get_environment_data',
         type: 'GET',
         dataType: 'json',
         success: function (data) {
            let echarts = layui.echarts;
	        var test = echarts.init(document.getElementById('test'),null, {
	        	width: 800,
	        	height: 400
	        });

	        const colorList = ["#9E87FF", '#73DDFF', '#fe9a8b', '#F56948', '#9E87FF']
	        option = {
				  visualMap: [
    					{
    					  show: false,
    					  type: 'continuous',
    					  seriesIndex: 0,
    					  min: 0,
    					  max: 400
    					},
    					{
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
  						    text: 'Gradient along the y axis'
  						  },
  						  {
  						    top: '55%',
  						    left: 'center',
  						    text: 'Gradient along the x axis'
  						  }
  						],
  						tooltip: {
  						  trigger: 'axis'
  						},
  						xAxis: [
  						  {
  						    data: data.date_time,
  						  },
  						  {
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
  						    showSymbol: false,
  						    data: data.total_active_power,
  						  },
  						  {
  						    type: 'line',
  						    showSymbol: false,
  						    data: data.total_active_power,
  						    xAxisIndex: 1,
  						    yAxisIndex: 1
  						  }
  						]

			}
			}
		 })

});