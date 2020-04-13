from django.shortcuts import render
import pandas as pd
import json
import datetime

ecdc_date = "12 de abril (ajustado)"
ecdc_file = "ecdc_cases_2020.04.12.csv"
confirmed_date = "12 de abril"
confirmed_file = "2020.04.12_confirmed_cases.csv"
suspected_date = "12 de abril"
suspected_file = "2020.04.12_suspected_cases.csv"

def get_context(dt, file_name):

    df = pd.read_csv("api_covid19/static/files/"+file_name)
    rs = df.groupby("Estado")["Edad"].count().reset_index() \
                      .sort_values('Edad', ascending=False) \
                      .set_index('Estado')
    estados = list(rs.index)
    values = list(rs.values)

    df['RangoDeEdad'] = df.Edad // 10
    rs = df.groupby("RangoDeEdad")["Edad"].count()
    rango_de_edad = list(rs.index)
    v_rango_de_edad = list(rs.values)

    edad_genero = []
    for i, v in enumerate(values):
        values[i] = values[i][0]

    edad_genero.append([0] * len(rango_de_edad))
    edad_genero.append([0] * len(rango_de_edad))
    print(edad_genero)

    rs_edad_genero = df.groupby(["RangoDeEdad", "Sexo"])["N° Caso"].count()
    cur_rango = ''
    i_rango=-1
    print(rs_edad_genero)
    for i, v in enumerate(rs_edad_genero):
        print(rs_edad_genero.index[i])
        if rs_edad_genero.index[i][0] != cur_rango:
            cur_rango=rs_edad_genero.index[i][0]
            i_rango=rango_de_edad.index(cur_rango)
        i_genero = (0 if rs_edad_genero.index[i][1] == "FEMENINO" else 1)
        edad_genero[i_genero][i_rango] = v
    print(edad_genero)

    v_edad_genero = []
    v_edad_genero.append({'name': 'FEMENINO', 'data': edad_genero[0]})
    v_edad_genero.append({'name': 'MASCULINO', 'data': edad_genero[1]})
    print(v_edad_genero)

    for i, v in enumerate(rango_de_edad):
        rango_de_edad[i] = str(rango_de_edad[i] * 10) + '-' + str((rango_de_edad[i] + 1) * 10)

    context = {"estados": estados, 'values': values, 'v_edad_genero': v_edad_genero,
               'rango_de_edad': rango_de_edad, 'v_rango_de_edad' : v_rango_de_edad, 'file_name': file_name, 'dt': dt}
    return context


def confirmed(request):
    context = get_context(confirmed_date, confirmed_file)
    return render(request, 'confirmed.html', context=context)


def suspected(request):
    context = get_context(suspected_date, suspected_file)
    #    table_content = df.to_html(index=None)
    #    table_content = table_content.replace("", "")
    #    table_content = table_content.replace('class="dataframe"', "class='table table-striped'")
    #    table_content = table_content.replace('border="1"', "")
    # 'table_data': table_content
    return render(request, 'suspected.html', context=context)


def index(request):
    df = pd.read_csv("api_covid19/static/files/" + ecdc_file)
    df.dropna(subset=['countryterritoryCode'], inplace=True)
    df = df[df['countryterritoryCode'].str.contains("MEX")]
    df = df[df['cases'] > 0]
    df['dateRep'] = pd.to_datetime(df['dateRep'], format='%d/%m/%Y')
    df['dateRep'] = df['dateRep']  + datetime.timedelta(days=-1)
    fechas = df['dateRep'].tolist()
    for i, v in enumerate(fechas):
        fechas[i] = fechas[i].strftime("%Y/%m/%d")
    fechas.reverse()
    cases = df['cases'].tolist()
    cases.reverse()
    deaths = df['deaths'].tolist()
    deaths.reverse()
    v_fechas = [{'name': 'Confirmados', 'data': cases}, {'name': 'Decesos', 'data': deaths}]
    cases_totals = []
    total = 0
    for i, v in enumerate(cases):
        total += v
        cases_totals.append(total)
    deaths_totals = []
    total = 0
    for i, v in enumerate(deaths):
        total += v
        deaths_totals.append(total)
    v_totals = [{'name': 'Confirmados', 'data': cases_totals}, {'name': 'Decesos', 'data': deaths_totals}]

    df = pd.read_csv("api_covid19/static/files/"+confirmed_file)
    for i, v in enumerate(df.columns):
        df.rename(columns={v: v.replace("\n", "")}, inplace=True)
    df['Fecha de Inicio de síntomas'] = pd.to_datetime(df['Fecha de Inicio de síntomas'], format='%d/%m/%Y')
    rs = df.groupby("Fecha de Inicio de síntomas")["N° Caso"].count()
    fechas_confirmed = list(rs.index)
    v_fechas_confirmed = list(rs.values)
    for i, v in enumerate(fechas_confirmed):
        fechas_confirmed[i] = fechas_confirmed[i].strftime("%Y/%m/%d")
    v_fechas2 = [{'name': 'Casos', 'data': v_fechas_confirmed,
                 'zoneAxis': 'x', 'zones': [{'value': 7}, {'dashStyle': 'dot', 'color': {
    'linearGradient': { 'x1': .25, 'x2': 1, 'y1': 0, 'y2': 0},
    'stops': [
        [0, '#FFDD33'],
        [1, 'white']
    ]
}}]}]
    context = {'fechas': fechas, 'v_fechas': v_fechas, 'fechas2': fechas_confirmed, 'v_fechas2': v_fechas2,
               'v_totals': v_totals,
               'file_name': ecdc_file, 'file_name2': confirmed_file, 'dt': confirmed_date, 'dt_ecdc': ecdc_date}
    return render(request, 'index.html', context=context)


def last_origin(request):
    dt = "7 de abril de 2020"
    file_name = "2020.04.07_confirmed_cases.csv"
    # read data

    df = pd.read_csv("api_covid19/static/files/"+file_name)
    rs = df.groupby("Estado")["Procedencia"].count().reset_index() \
                      .sort_values('Procedencia', ascending=False) \
                      .set_index('Estado')
    estados = list(rs.index)
    values = list(rs.values)
    rs = df.groupby("Procedencia")["Estado"].count().reset_index() \
                      .sort_values('Estado', ascending=False) \
                      .set_index('Procedencia')
    procedencia = list(rs.index)
    v_procedencia = list(rs.values)
    rs_estado_origen = df.groupby(["Estado", "Procedencia"])["N° Caso"].count()
    df['RangoDeEdad'] = df.Edad // 10
        # str((df["Edad"] % 10)*10) + '-' + str(((df["Edad"] % 10)+1)*10)
    rs = df.groupby("RangoDeEdad")["Procedencia"].count()
    rango_de_edad = list(rs.index)
    v_rango_de_edad = list(rs.values)
    print(rango_de_edad)
    print(v_rango_de_edad)
    proced = []
    for i, v in enumerate(values):
        values[i] = values[i][0]
    for i, v in enumerate(rango_de_edad):
        rango_de_edad[i] = str(rango_de_edad[i] * 10) + '-' + str((rango_de_edad[i] + 1) * 10)
    for i, v in enumerate(v_procedencia):
        v_procedencia[i] = v_procedencia[i][0]
        proced.append([0] * len(estados))
    # for i, v in enumerate(v_rango_de_edad):
    #     v_rango_de_edad[i] = v_rango_de_edad[i][0]
    cur_pais = ''

    print(rango_de_edad)
    print(v_rango_de_edad)
    for i, v in enumerate(rs_estado_origen):
        if rs_estado_origen.index[i][0]!=cur_pais:
            cur_pais=rs_estado_origen.index[i][0]
            i_estado=estados.index(cur_pais)
        proced[procedencia.index(rs_estado_origen.index[i][1])][i_estado] = v

    v_estado_origen = []
    for i, v in enumerate(procedencia):
        v_estado_origen.append({'name': v, 'data': proced[i]})

    if "Estados" in estados:
        i=estados.index("Estados")
        estados[i]="EEUU"
        print(i)
        print(estados[i])

    values_origen = [{'name': 'Casos por origen', 'data': values}]
    context = {"estados": estados, "procedencia": procedencia, "v_procedencia": v_procedencia,
               'values': values, 'values_origen': values_origen, 'v_estado_origen' : v_estado_origen,
               'rango_de_edad': rango_de_edad, 'v_rango_de_edad' : v_rango_de_edad,
               'file_name': file_name, 'dt': dt}
    return render(request, 'last_from.html', context=context)
