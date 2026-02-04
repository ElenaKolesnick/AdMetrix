// static/js/charts.js
function renderCharts() {
    const config = {responsive: true, displayModeBar: false};

    // Читаем данные из безопасных JSON-контейнеров
    const mapData = JSON.parse(document.getElementById('map-data-json').textContent);
    const spendData = JSON.parse(document.getElementById('spend-data-json').textContent);
    const channelData = JSON.parse(document.getElementById('channel-data-json').textContent);

    if (mapData && mapData.data) {
        Plotly.newPlot('map-chart', mapData.data, mapData.layout, config);
    }
    if (spendData && spendData.data) {
        Plotly.newPlot('spend-chart', spendData.data, spendData.layout, config);
    }
    if (channelData && channelData.data) {
        Plotly.newPlot('channel-chart', channelData.data, channelData.layout, config);
    }
}

// Запускаем отрисовку
document.addEventListener('DOMContentLoaded', renderCharts);