/*
* AdMetrix Custom Dashboard Logic
* Based on Bootstrap 5
*/

"use strict";
const d = document;
d.addEventListener("DOMContentLoaded", function(event) {

    // Инициализация всплывающих подсказок (Tooltips)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Инициализация поповеров (Popovers)
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl)
    })

    // Логика сайдбара для мобильных устройств
    const breakpoints = { sm: 540, md: 720, lg: 960, xl: 1140 };
    var sidebar = document.getElementById('sidebarMenu')
    if(sidebar && d.body.clientWidth < breakpoints.lg) {
        sidebar.addEventListener('shown.bs.collapse', function () {
            document.querySelector('body').style.position = 'fixed';
        });
        sidebar.addEventListener('hidden.bs.collapse', function () {
            document.querySelector('body').style.position = 'relative';
        });
    }

    // Динамическая установка фона (если используется в шаблоне)
    [].slice.call(d.querySelectorAll('[data-background]')).map(function(el) {
        el.style.background = 'url(' + el.getAttribute('data-background') + ')';
    });

    // Плавный скролл для якорей
    var scroll = new SmoothScroll('a[href*="#"]', {
        speed: 500,
        speedAsDuration: true
    });

    // Автоматическая установка текущего года в футере
    if(d.querySelector('.current-year')){
        d.querySelector('.current-year').textContent = new Date().getFullYear();
    }
    
    // Графики Chartist (оставляем только если они вам нужны в report.html)
    if(d.querySelector('.ct-chart-sales-value')) {
        new Chartist.Line('.ct-chart-sales-value', {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            series: [[0, 10, 30, 40, 80, 60, 100]]
        }, {
            low: 0, showArea: true, fullWidth: true,
            axisX: { position: 'end', showGrid: true },
            axisY: { showGrid: false, showLabel: false }
        });
    }
});
