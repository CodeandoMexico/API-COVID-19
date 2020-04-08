Highcharts.chart('container_origen', {
chart: {
      type: 'column'
},
title: {
      text: 'Casos por Procedencia'
},
subtitle: {
      text: ''
},
xAxis: {
      categories: _procedencia,
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
                y: -15
            },
            pointPadding: 0.1,
            groupPadding: 0
        }
},
series: [{
      name: 'Núm. Casos',
      data: _v_procedencia
}]
});