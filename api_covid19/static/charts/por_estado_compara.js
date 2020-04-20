Highcharts.chart('container_compara', {
chart: {
      type: 'column'
},
    colors: ['#E76C7C', '#C70039', '#FFDD33'],
    legend:{ enabled:true },
title: {
      text:  _case_type + ' reportados por Estados vs SSA Datos Abiertos'
},
subtitle: {
      text: _dt + ' - puede reflejar diferentes horarios de corte'
},
xAxis: {
      categories: _edos_compara,
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
series: _v_compara
});