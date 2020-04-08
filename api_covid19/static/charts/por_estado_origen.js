Highcharts.chart('container_estado_origen', {
chart: {
      type: 'bar'
},
title: {
      text: 'Casos por Estado y Origen de Viaje'
},
subtitle: {
      text: ''
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
      shared: false,
      useHTML: true
},
plotOptions: {
        series: {
            stacking: 'normal',
            dataLabels: {
                enabled: true,
                formatter: function(){
                    console.log(this);
                    var val = this.y;
                    if (val < 6) {
                        return '';
                    }
                    return val;
                },
                color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
            },
        }
},
series: _v_estado_origen
});