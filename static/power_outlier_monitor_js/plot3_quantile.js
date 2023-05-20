layui.use(['echarts'], function() {
    $.ajax({
        url: '/get_threshold_data',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let echarts = layui.echarts;
            var plot3_quantile = echarts.init(document.getElementById('plot3_quantile'), null, {
                width: 800,
                height: 400
            });
            option = {
                title: {
                  text: '分位数阈值异常数据检测'
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
                    data: data.normal_data_quantile,  // 正常数据
                    itemStyle: {
                        color: '#5d6fc2'  // 正常数据的标记颜色
                    },
                    symbolSize: 5
                }, {
                    type: 'scatter',
                    data: data.anomaly_data_quantile,  // 异常数据
                    itemStyle: {
                        color: '#d14a61'  // 异常数据的标记颜色
                    },
                    symbolSize: 5
                }]
            };
            plot3_quantile.setOption(option);
	        window.onresize = function() {
            plot3_quantile.resize();
        }
        }
    })
})