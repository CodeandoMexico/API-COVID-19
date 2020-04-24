from django.shortcuts import render
import pandas as pd
import json
import sqlite3
import os
import datetime
import math

files_path = "api_covid19/static/files/"
today = datetime.date.today()
dia_ext = today.strftime("%d") + " de abril"
dia_punto = today.strftime("%m.%d")
dia = today.strftime("%m%d")
dt_compara = '23 de abril'
compara_file = "DATOS_Entidades_2020.04.23.csv"

ecdc_date = ""
ecdc_file = ""
file_da = ""
dt_da = ""

def update_dates():
    global ecdc_date, ecdc_file, file_da, dt_da
    yesterday = today - datetime.timedelta(days=1)
    ant_dia_ext = yesterday.strftime("%d") + " de abril"
    ant_dia_punto = yesterday.strftime("%m.%d")
    ant_dia = yesterday.strftime("%m%d")
    if os.path.exists(files_path + f"ecdc_cases_2020.{dia_punto}.csv"):
        ecdc_date = dia_ext + " (ajustado)"
        ecdc_file = f"ecdc_cases_2020.{dia_punto}.csv"
    else:
        ecdc_date = ant_dia_ext + " (ajustado)"
        ecdc_file = f"ecdc_cases_2020.{ant_dia_punto}.csv"
    if os.path.exists(files_path + f"20{dia}COVID19MEXICO.csv"):
        file_da = f"20{dia}COVID19MEXICO.csv"
        dt_da = dia_ext
    else:
        file_da = f"20{ant_dia}COVID19MEXICO.csv"
        dt_da = ant_dia_ext

def confirmed(request):
    update_dates()
    conn = sqlite3.connect("covid19mx.db")
    cur = conn.cursor()
    cur.execute("SELECT ENTIDAD_FEDERATIVA, count(*) as CONFIRMED FROM datos_abiertos_MX d " +
                "JOIN Catalogo_Entidades e ON d.ENTIDAD_UM = e.CLAVE_ENTIDAD " +
                "WHERE RESULTADO = 1 GROUP BY ENTIDAD_FEDERATIVA ORDER BY count(*) DESC")
    estados = []
    values = []
    for row in cur:
        estados.append(row[0])
        values.append(row[1])

    v_edad_genero = []
    rango_de_edad = []
    por_rango_fem = []
    por_rango_mas = []
    por_rango_sin = []
    v_rango_de_edad = []
    cats = []
    v_cats = []
    cats2 = []
    v_cats2 = []

    cur.execute("SELECT (EDAD/10) || '0 - ' || (EDAD/10 + 1) || '0' as RANGO_EDAD, c.DESCRIPCIÓN, count(*) as DEATHS "
                "FROM datos_abiertos_MX d JOIN Catalogo_Sexo c ON d.SEXO = c.CLAVE "
                "WHERE RESULTADO = 1 "
                "GROUP BY (EDAD/10) || '0 - ' || (EDAD/10 + 1) || '0', SEXO ORDER BY EDAD/10 ")
    cur_rango = ''
    for row in cur:
        if cur_rango != row[0]:
            cur_rango = row[0]
            if len(por_rango_fem) < len(rango_de_edad):
                por_rango_fem.append(0)
            if len(por_rango_mas) < len(rango_de_edad):
                por_rango_mas.append(0)
            if len(por_rango_sin) < len(rango_de_edad):
                por_rango_sin.append(0)
            rango_de_edad.append(row[0])
        if row[1] == "MUJER":
            por_rango_fem.append(row[2])
        elif row[1] == "HOMBRE":
            por_rango_mas.append(row[2])
        else:
            por_rango_sin.append(row[2])

    if len(por_rango_fem) < len(rango_de_edad):
        por_rango_fem.append(0)
    if len(por_rango_mas) < len(rango_de_edad):
        por_rango_mas.append(0)
    if len(por_rango_sin) < len(rango_de_edad):
        por_rango_sin.append(0)

    for i, v in enumerate(rango_de_edad):
        v_rango_de_edad.append(por_rango_fem[i] + por_rango_mas[i] + por_rango_sin[i])

    v_edad_genero.append({'name': 'FEMENINO', 'data': por_rango_fem})
    v_edad_genero.append({'name': 'MASCULINO', 'data': por_rango_mas})
    if sum(por_rango_sin) > 0:
        v_edad_genero.append({'name': 'NO DEFINIDO', 'data': por_rango_sin})

    cur.execute("SELECT "
                "COUNT(CASE WHEN EDAD >= 60 THEN 1 END) AS '>= 60 AÑOS', "
                "COUNT(CASE WHEN HIPERTENSION = 1 THEN 1 END) AS HIPERTENSION, "
                "COUNT(CASE WHEN OBESIDAD = 1 THEN 1 END) AS OBESIDAD, "
                "COUNT(CASE WHEN DIABETES = 1 THEN 1 END) AS DIABETES, "
                "COUNT(CASE WHEN TABAQUISMO = 1 THEN 1 END) AS TABAQUISMO, "
                "COUNT(CASE WHEN EMBARAZO = 1 THEN 1 END) AS EMBARAZO, "
                "COUNT(CASE WHEN INTUBADO = 1 THEN 1 END) AS INTUBADO, "
                "COUNT(CASE WHEN UCI = 1 THEN 1 END) AS 'EN UCI', "
                "COUNT(CASE WHEN INTUBADO = 1 OR UCI = 1 THEN 1 END) AS 'INTUBADO O UCI' "
                "FROM datos_abiertos_MX WHERE RESULTADO = 1 ")
    col_names = list(map(lambda x: x[0], cur.description))
    for row in cur:
        for i, v in enumerate(row):
            cats.append(col_names[i])
            v_cats.append(row[i])

    n_criticos = v_cats[len(v_cats)-1]

    cur.execute("SELECT "
                "COUNT(CASE WHEN EDAD >= 60 THEN 1 END) AS '>= 60 AÑOS', "
                "COUNT(CASE WHEN HIPERTENSION = 1 THEN 1 END) AS HIPERTENSION, "
                "COUNT(CASE WHEN OBESIDAD = 1 THEN 1 END) AS OBESIDAD, "
                "COUNT(CASE WHEN DIABETES = 1 THEN 1 END) AS DIABETES, "
                "COUNT(CASE WHEN TABAQUISMO = 1 THEN 1 END) AS TABAQUISMO, "
                "COUNT(CASE WHEN EMBARAZO = 1 THEN 1 END) AS EMBARAZO "
                "FROM datos_abiertos_MX WHERE RESULTADO = 1 AND (INTUBADO = 1 OR UCI = 1)")
    col_names = list(map(lambda x: x[0], cur.description))
    for row in cur:
        for i, v in enumerate(row):
            cats2.append(col_names[i])
            v_cats2.append(row[i])
    cur.close()
    conn.close()
    context = {'n_total': sum(values), "estados": estados, 'values': values, 'v_edad_genero': v_edad_genero,
               'rango_de_edad': rango_de_edad, 'v_rango_de_edad' : v_rango_de_edad, 'file_name': file_da, 'dt': dt_da,
               "cats": cats, 'v_cats': v_cats, "cats2": cats2, 'v_cats2': v_cats2, 'n_criticos': n_criticos}

    return render(request, 'confirmed.html', context=context)

def deaths(request):
    update_dates()
    conn = sqlite3.connect("covid19mx.db")
    cur = conn.cursor()
    # cur.execute("SELECT ENTIDAD_UM, count(*) as DEATHS FROM datos_abiertos_MX d " +
    #             "WHERE RESULTADO = 1 AND FECHA_DEF <> '9999-99-99' GROUP BY ENTIDAD_UM ORDER BY count(*) DESC")
    cur.execute("SELECT ENTIDAD_FEDERATIVA, count(*) as DEATHS FROM datos_abiertos_MX d " +
                "JOIN Catalogo_Entidades e ON d.ENTIDAD_UM = e.CLAVE_ENTIDAD " +
                "WHERE RESULTADO = 1 AND FECHA_DEF <> '9999-99-99' GROUP BY ENTIDAD_FEDERATIVA ORDER BY count(*) DESC")
    estados = []
    values = []
    for row in cur:
        estados.append(row[0])
        values.append(row[1])
#    cur.close()

    v_edad_genero = []
    rango_de_edad = []
    por_rango_fem = []
    por_rango_mas = []
    por_rango_sin = []
    v_rango_de_edad = []
    cats = []
    v_cats = []
    cats2 = []
    v_cats2 = []

    cur.execute("SELECT (EDAD/10) || '0 - ' || (EDAD/10 + 1) || '0' as RANGO_EDAD, c.DESCRIPCIÓN, count(*) as DEATHS "
                "FROM datos_abiertos_MX d JOIN Catalogo_Sexo c ON d.SEXO = c.CLAVE "
                "WHERE RESULTADO = 1 AND FECHA_DEF <> '9999-99-99' "
                "GROUP BY (EDAD/10) || '0 - ' || (EDAD/10 + 1) || '0', SEXO ORDER BY EDAD/10 ")
    cur_rango = ''
    for row in cur:
        if cur_rango != row[0]:
            cur_rango = row[0]
            if len(por_rango_fem) < len(rango_de_edad):
                por_rango_fem.append(0)
            if len(por_rango_mas) < len(rango_de_edad):
                por_rango_mas.append(0)
            if len(por_rango_sin) < len(rango_de_edad):
                por_rango_sin.append(0)
            rango_de_edad.append(row[0])
        if row[1] == "MUJER":
            por_rango_fem.append(row[2])
        elif row[1] == "HOMBRE":
            por_rango_mas.append(row[2])
        else:
            por_rango_sin.append(row[2])

    if len(por_rango_fem) < len(rango_de_edad):
        por_rango_fem.append(0)
    if len(por_rango_mas) < len(rango_de_edad):
        por_rango_mas.append(0)
    if len(por_rango_sin) < len(rango_de_edad):
        por_rango_sin.append(0)

    cur.execute("SELECT "
                "COUNT(CASE WHEN EDAD >= 60 THEN 1 END) AS '>= 60 AÑOS', "
                "COUNT(CASE WHEN HIPERTENSION = 1 THEN 1 END) AS HIPERTENSION, "
                "COUNT(CASE WHEN OBESIDAD = 1 THEN 1 END) AS OBESIDAD, "
                "COUNT(CASE WHEN DIABETES = 1 THEN 1 END) AS DIABETES, "
                "COUNT(CASE WHEN INTUBADO = 1 THEN 1 END) AS INTUBADO, "
                "COUNT(CASE WHEN TABAQUISMO = 1 THEN 1 END) AS TABAQUISMO, "
                "COUNT(CASE WHEN EMBARAZO = 1 THEN 1 END) AS EMBARAZO "
                "FROM datos_abiertos_MX WHERE RESULTADO = 1 AND FECHA_DEF <> '9999-99-99'")
    col_names = list(map(lambda x: x[0], cur.description))
    for row in cur:
        for i, v in enumerate(row):
            cats.append(col_names[i])
            v_cats.append(row[i])

    cur.execute("SELECT "
                "COUNT(CASE WHEN EDAD >= 60 THEN 1 END) AS '>= 60 AÑOS', "
                "COUNT(CASE WHEN HIPERTENSION = 1 THEN 1 END) AS HIPERTENSION, "
                "COUNT(CASE WHEN OBESIDAD = 1 THEN 1 END) AS OBESIDAD, "
                "COUNT(CASE WHEN DIABETES = 1 THEN 1 END) AS DIABETES, "
                "COUNT(CASE WHEN INTUBADO = 1 THEN 1 END) AS INTUBADO, "
                "COUNT(CASE WHEN TABAQUISMO = 1 THEN 1 END) AS TABAQUISMO, "
                "COUNT(CASE WHEN EMBARAZO = 1 THEN 1 END) AS EMBARAZO "
                "FROM datos_abiertos_MX WHERE RESULTADO = 1 AND FECHA_DEF <> '9999-99-99' AND INTUBADO = 1 OR UCI = 1 ")
    col_names = list(map(lambda x: x[0], cur.description))
    for row in cur:
        for i, v in enumerate(row):
            cats2.append(col_names[i])
            v_cats2.append(row[i])

    cur.close()
    conn.close()
    for i, v in enumerate(rango_de_edad):
        v_rango_de_edad.append(por_rango_fem[i] + por_rango_mas[i] + por_rango_sin[i])

    v_edad_genero.append({'name': 'FEMENINO', 'data': por_rango_fem})
    v_edad_genero.append({'name': 'MASCULINO', 'data': por_rango_mas})
    if sum(por_rango_sin) > 0:
        v_edad_genero.append({'name': 'NO DEFINIDO', 'data': por_rango_sin})

    df = pd.read_csv(files_path + compara_file, encoding = "latin")
    edos_compara = df['ENTIDAD_FEDERATIVA'].tolist()
    dece_compara = df['DECESOS'].tolist()
    abie_compara = []
    difs_compara = []
    to_del = []
    for i, v in enumerate(edos_compara):
        if math.isnan(dece_compara[i]) or dece_compara[i] == "" or dece_compara[i] <= values[estados.index(v)]:
            dece_compara[i] = 0
            abie_compara.append(0)
            difs_compara.append(0)
            to_del.append(i)
        else:
            abie_compara.append(values[estados.index(v)])
            difs_compara.append(dece_compara[i] - values[estados.index(v)])
    to_del.reverse()
    for i in to_del:
        edos_compara.pop(i)
        dece_compara.pop(i)
        abie_compara.pop(i)
        difs_compara.pop(i)

    v_compara = [{'name': 'Datos de Estados', 'data': dece_compara},
                 {'name': 'SSA Datos Abiertos', 'data': abie_compara},
                 {'name': 'Diferencia', 'data': difs_compara}]
    context = {"estados": estados, 'values': values, "cats": cats, 'v_cats': v_cats,
               "cats2": cats2, 'v_cats2': v_cats2, 'v_edad_genero': v_edad_genero,
               'rango_de_edad': rango_de_edad, 'v_rango_de_edad' : v_rango_de_edad, 'file_da': file_da, 'dt': dt_da,
               'n_total': sum(values), 'edos_compara': edos_compara, 'v_compara': v_compara, 'dt_compara': dt_compara,
               'n_sum_difs': round(sum(difs_compara))}
    return render(request, 'deaths.html', context=context)

def index(request):
    update_dates()
    print("ECDC FILES ----------------")
    print(ecdc_file)
    df = pd.read_csv(files_path + ecdc_file)
    df.dropna(subset=['countryterritoryCode'], inplace=True)
    df = df[df['countryterritoryCode'].str.contains("MEX")]
    df = df[df['cases'] > 0]
    df['dateRep'] = pd.to_datetime(df['dateRep'], format='%d/%m/%Y')
    df['dateRep'] = df['dateRep']  + datetime.timedelta(days=-1)
    fechas = df['dateRep'].tolist()
    fechas.reverse()
    cases = df['cases'].tolist()
    cases.reverse()
    deaths = df['deaths'].tolist()
    deaths.reverse()
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

    conn = sqlite3.connect("covid19mx.db")
    cur = conn.cursor()
    cur.execute("SELECT  (SELECT COUNT(*) FROM datos_abiertos_MX WHERE RESULTADO = 1) as Confirmados" +
        ", (SELECT COUNT(*) FROM datos_abiertos_MX WHERE RESULTADO = 1 AND FECHA_DEF <> '9999-99-99') as Decesos")
    rows = cur.fetchall()
    print(rows)
    print(rows[0][0])
    if cases_totals[len(cases_totals)-1] < rows[0][0]:
        new_cases = rows[0][0] - cases_totals[len(cases_totals)-1]
        new_deaths = rows[0][1] - deaths_totals[len(deaths_totals)-1]
        cases.append(new_cases)
        deaths.append(new_deaths)
        cases_totals.append(rows[0][0])
        deaths_totals.append(rows[0][1])
        fechas.append(fechas[len(fechas)-1] + datetime.timedelta(days=1))
    cur.close()
    conn.close()

    for i, v in enumerate(fechas):
        fechas[i] = fechas[i].strftime("%Y/%m/%d")
    #
    # df = pd.read_csv("api_covid19/static/files/"+confirmed_file)
    # for i, v in enumerate(df.columns):
    #     df.rename(columns={v: v.replace("\n", "")}, inplace=True)
    # df['Fecha de Inicio de síntomas'] = pd.to_datetime(df['Fecha de Inicio de síntomas'], format='%d/%m/%Y')
    # rs = df.groupby("Fecha de Inicio de síntomas")["N° Caso"].count()
    # fechas_confirmed = list(rs.index)
    # v_fechas_confirmed = list(rs.values)
    # for i, v in enumerate(fechas_confirmed):
    #     fechas_confirmed[i] = fechas_confirmed[i].strftime("%Y/%m/%d")
    # v_fechas2 = [{'name': 'Casos', 'data': v_fechas_confirmed,
    #              'zoneAxis': 'x', 'zones': [{'value': 7}, {'dashStyle': 'dot', 'color': {
    #              'linearGradient': { 'x1': .25, 'x2': 1, 'y1': 0, 'y2': 0},
    #              'stops': [ [0, '#FFDD33'], [1, 'white'] ]
    #             }}]}]

    cases[len(cases)-1] = {"y": cases[len(cases)-1], "dataLabels":{"enabled":"true"}}
    deaths[len(deaths)-1] = {"y": deaths[len(deaths)-1], "dataLabels":{"enabled":"true"}}
    v_fechas = [{'name': 'Confirmados', 'data': cases}, {'name': 'Decesos', 'data': deaths}]

    cases_totals[len(cases_totals)-1] = {"y": cases_totals[len(cases_totals)-1], "dataLabels":{"enabled":"true"}}
    deaths_totals[len(deaths_totals)-1] = {"y": deaths_totals[len(deaths_totals)-1], "dataLabels":{"enabled":"true"}}
    v_totals = [{'name': 'Confirmados', 'data': cases_totals}, {'name': 'Decesos', 'data': deaths_totals}]

    context = {'fechas': fechas, 'v_fechas': v_fechas, 'fechas2': [], 'v_fechas2': [],
               'v_totals': v_totals,
               'file_name': ecdc_file, 'file_name2': file_da, 'dt': dt_da, 'dt_ecdc': ecdc_date}
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
