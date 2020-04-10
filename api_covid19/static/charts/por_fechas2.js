Highcharts.chart('container_fechas2', {
    chart: {
        type: 'area'
    },
    colors: ['#FFDD33'],
title: {
      text: 'Info de Casos Conocidos'
},
subtitle: {
      text: 'Fuente: Gob. de MX al ' + _dt
},
xAxis: {
      categories: _fechas2,
      crosshair: true
},
yAxis: {
      min: 0,
      title: {
  text: 'Casos'
      }
},
tooltip: {
      headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
      pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
  '<td style="padding:0"><b>{point.y}</b></td></tr>',
      footerFormat: '</table>',
      shared: true,
      useHTML: true
},
plotOptions: {
      column: {
          pointPadding: 0.2,
          borderWidth: 0
        },
        series: {
            dataLabels: {
                enabled: true,
                align: 'right',
                color: '#444444',
                rotation: -90,
                y: -14
            },
            pointPadding: 0.1,
            groupPadding: 0
        }
},
series: _v_fechas2
});