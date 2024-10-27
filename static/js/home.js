// 页面加载时自动弹出模态框并监听点击事件
window.onload = function () {
	openModal();
};

function openModal() {
			
	document.getElementById('overlay').style.display = 'block';
    document.getElementById('modal').style.display = 'block';
	document.getElementById('overlay').addEventListener('click', function (event) {
    if (event.target === document.getElementById('overlay')) {
		closeModal();
        }
    });
}

function closeModal() {
	document.getElementById('overlay').style.display = 'none';
    document.getElementById('modal').style.display = 'none';
}

// 异步获取图表数据
async function fetchChartData() {
    try {
        const response = await fetch('/get_chart_data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching chart data:', error);
        return null;
    }
}

// 更新图表数据
async function updateChartData() {
    const chartData = await fetchChartData();

    if (chartData) {
        // 使用ApexCharts库来创建折线图
        var chart = new ApexCharts(document.querySelector("#chart"), {
            series: chartData.series,
            chart: {
                height: 200, // 设置图表高度
                type: 'line',
                background: 'transparent', // 将图表背景设为透明
            },
            xaxis: {
                categories: chartData.categories,
            },
			// 添加曲线属性
            stroke: {
                curve: 'smooth', // 使用平滑曲线
            },
        });

        chart.render();
    }
}

// 初始加载图表数据
updateChartData();

// 点击用户图标时显示或隐藏选项列表
$('.userico').click(function() {
    $('.userico_options').fadeToggle('fast');
});

// 鼠标移出选项列表时隐藏
$('.userico_options').mouseleave(function() {
    $(this).fadeOut('fast');
});

