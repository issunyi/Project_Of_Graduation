layui.use(['echarts'], function() {
    $.ajax({
        url: '/get_threshold_data',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let echarts = layui.echarts;
            var plot2_max_min = echarts.init(document.getElementById('plot2_max_min'), null, {
                width: 800,
                height: 400
            });
            option = {
                title: {
                  text: '最值阈值异常数据检测'
                },
                tooltip: {
                  trigger: 'axis'
                },
                legend: {
                  data: ['正常数据', '异常数据']
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
                  type: 'time',
                },
                yAxis: {
                  type: 'value'
                },
                series: [{
                    type: 'scatter',
                    data: data.normal_data_max_min,  // 正常数据
                    itemStyle: {
                        color: '#5d6fc2'  // 正常数据的标记颜色
                    },
                    symbolSize: 5
                }, {
                    type: 'scatter',
                    data: data.anomaly_data_max_min,  // 异常数据
                    itemStyle: {
                        color: '#d14a61'  // 异常数据的标记颜色
                    },
                    symbolSize: 5
                }]
            };
            plot2_max_min.setOption(option);
	        window.onresize = function() {
            plot2_max_min.resize();
        }
        }
    })
})