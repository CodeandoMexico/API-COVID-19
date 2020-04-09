Highcharts.chart('container', {
chart: {
      type: 'column'
},
title: {
      text: 'Casos por Estado'
},
subtitle: {
      text: _dt
},
xAxis: {
      categories: _estados,
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
series: [{
      name: 'Casos',
      data: _values
}]
});