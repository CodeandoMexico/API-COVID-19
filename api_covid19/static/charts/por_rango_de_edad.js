Highcharts.chart('container_rango_de_edad', {
chart: {
      type: 'column'
},
colors: ['#3B97B2', '#67BC42', '#FF56DE', '#E6D605', '#BC36FE'] ,

title: {
      text: 'Casos por Rango de Edad'
},
subtitle: {
      text: ''
},
xAxis: {
      categories: _rango_de_edad,
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
          borderWidth: 0,
          colorByPoint: true
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
      data: _v_rango_de_edad
}]
});