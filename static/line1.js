layui.use(['echarts'], function() {
     $.ajax({
		 url: '/get_environment_data',
		 type: 'GET',
		 dataType: 'json',
		 success: function (data) {
			let echarts = layui.echarts;
			var line2 = echarts.init(document.getElementById('line2'),null, {
				width: 850,
				height: 400
			});


			tick_dates = []
    		curr_date = new Date(data.min_date);
    		while (curr_date <= new Date(data.max_date)) {
        		tick_dates.push(curr_date.toISOString().slice(0, 10));
        		curr_date.setDate(curr_date.getDate() + 1);
    		}

			const colorList = ["#9E87FF", '#73DDFF', '#fe9a8b', '#F56948', '#9E87FF']
			option = {
				backgroundColor: '#fff',
				title: {
					text: '最高温度',
					fontSize: 12,
					fontWeight: 400,
					left: '18px',
					right: '4%',
					top: '1%',
				},
				legend: {
					icon: 'circle',
					top: '5%',
					right: '5%',
					itemWidth: 6,
					itemGap: 20,
					color: '#556677'
				},
				tooltip: {
					trigger: 'axis',
					axisPointer: {
						label: {
							show: true,
							backgroundColor: '#fff',
							color: '#556677',
							borderColor: 'rgba(0,0,0,0)',
							shadowColor: 'rgba(0,0,0,0)',
							shadowOffsetY: 0
						},
						lineStyle: {
							width: 0
						}
					},
					backgroundColor: '#fff',
					color: '#5c6c7c',
					padding: [10, 10],
					extraCssText: 'box-shadow: 1px 0 2px 0 rgba(163,163,163,0.5)'
				},
				grid: {
					top: '20%',
					left: '3%',
				},
				xAxis: [{
					type: 'category',
					data: data.date_time,
					gridIndex: 1,
					// data: tick_dates,
					// min: data.min_date,
					// max: data.max_date,
					axisLine: {
						lineStyle: {
							color: '#DCE2E8'
						}
					},
					axisTick: {
						show: false
					},
					axisLabel: {
						interval: 0,
						color: '#556677',
						// 默认x轴字体大小
						fontSize: 12,
						// margin:文字到x轴的距离
						margin: 15,
						rotate: 45,
					},
					axisPointer: {
						label: {
							// padding: [11, 5, 7],
							padding: [0, 0, 10, 0],

							// 这里的margin和axisLabel的margin要一致!
							margin: 15,
							// 移入时的字体大小
							fontSize: 12,
							backgroundColor: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0,
									color: '#fff' // 0% 处的颜色
								}, {
									// offset: 0.9,
									offset: 0.86,

									color: '#fff' // 0% 处的颜色
								}, {
									offset: 0.86,
									color: '#33c0cd' // 0% 处的颜色
								}, {
									offset: 1,
									color: '#33c0cd' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							}
						}
					},
					boundaryGap: false
				}],
				yAxis: [{
					type: 'value',
					axisTick: {
						show: false
					},
					axisLine: {
						show: true,
						lineStyle: {
							color: '#DCE2E8'
						}
					},
					axisLabel: {
						color: '#556677',
					},
					splitLine: {
						show: false
					}
				}, {
					type: 'value',
					position: 'right',
					axisTick: {
						show: false
					},
					axisLabel: {
						color: '#556677',
						formatter: '{value}'
					},
					axisLine: {
						show: true,
						lineStyle: {
							color: '#DCE2E8'
						}
					},
					splitLine: {
						show: false
					}
				}],
				series: [{
						name: '最高温度',
						type: 'line',
						data: data.highest_temp,
						symbolSize: 1,
						symbol: 'circle',
						smooth: false,
						yAxisIndex: 0,
						showSymbol: true,
						lineStyle: {
							width: 2,
							color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [{
									offset: 0,
									color: '#9effff'
								},
								{
									offset: 1,
									color: '#9E87FF'
								}
							]),
							shadowColor: 'rgba(158,135,255, 0.3)',
							shadowBlur: 10,
							shadowOffsetY: 20
						},
						itemStyle: {
							color: colorList[0],
							borderColor: colorList[0]
						}

					}
				]
			};

			line2.setOption(option);

			window.onresize = function() {
				line2.resize();
			}
		 }

	 })
})