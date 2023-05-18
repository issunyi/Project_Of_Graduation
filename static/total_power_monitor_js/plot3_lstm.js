layui.use(['echarts'], function() {
    $.ajax({
        url: '/lstm',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let echarts = layui.echarts;
            var plot3_lstm = echarts.init(document.getElementById('plot3_lstm'), null, {
                width: 1000,
                height: 400
            });
            console.log(data.x)
            console.log(data.truth)
            console.log(data.predict)
            var colors = ['#d14a61','#289ddc','#675bba'];
            option = {
                color: colors,
                title: {
                  text: 'LSTM模型负载功率预测'
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
                  data: data.x
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
                    name: 'LSTM模型预测负载功率值',
                    type: 'line',
                    showSymbol: false,
                    data: data.predict,
                  },{
                    name: '实际功率值',
                    type: 'scatter',
                    showSymbol: false,
                    data: data.truth
                  }

                ]
            };
            plot3_lstm.setOption(option);
	         window.onresize = function() {
	    	    plot3_lstm.resize();
	        }

        }
    })
})
