Highcharts.chart('container_edad_genero', {
chart: {
      type: 'bar'
},
title: {
      text: _case_type + ' por Genero y Rango de Edad'
},
colors: _colors_genero_edad ,
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
      shared: false,
      useHTML: true
},
plotOptions: {
        series: {
            stacking: 'normal',
            dataLabels: {
                enabled: true,
                formatter: function(){
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
series: _v_edad_genero
});