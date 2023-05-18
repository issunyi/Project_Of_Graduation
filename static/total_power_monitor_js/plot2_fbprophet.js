layui.use(['echarts'], function() {
    $.ajax({
        url: '/fbprophet',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let echarts = layui.echarts;
            var plot2_fbprophet = echarts.init(document.getElementById('plot2_fbprophet'), null, {
                width: 1000,
                height: 400
            });

            // console.log(data.x_valid)
            // console.log(data.y_pred)
            // console.log(data.y_valid)

            var colors = ['#5793f3', '#d14a61', '#675bba'];
            option = {
                color: colors,
                title: {
                  text: 'fbprophet模型负载功率预测'
                },
                tooltip: {
                  trigger: 'axis',
                },
                toolbox: {
                    feature: {
                     saveAsImage: {}
                 }
                 },
                xAxis: {
                  type: 'category',
                  boundaryGap: false,
                  data: data.x_valid
                },
                yAxis: {
                  type: 'value',
                  boundaryGap: [0, '100%'],
                  splitLine: {
                    show: false
                  }
                },
                series: [
                  {
                    name: 'fbprophet模型预测负载功率值',
                    type: 'line',
                    showSymbol: false,
                    data: data.y_pred,
                  },{
                    name: '实际功率值',
                    type: 'scatter',
                    showSymbol: false,
                    data: data.y_valid
                  }

                ]
            };
            plot2_fbprophet.setOption(option);
	         window.onresize = function() {
	    	    plot2_fbprophet.resize();
	        }

        }
    })
})







