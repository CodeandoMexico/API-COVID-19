from django.shortcuts import render
import pandas as pd
import json

def get_context(dt, file_name):

    df = pd.read_csv("api_covid19/files/"+file_name)
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

def index(request):
    dt = "9 de abril de 2020"
    file_name = "2020.04.09_confirmed_cases.csv"
    context = get_context(dt, file_name)
    return render(request, 'index.html', context=context)


def suspected(request):

    dt = "9 de abril de 2020"
    file_name = "2020.04.09_suspected_cases.csv"
    context = get_context(dt, file_name)
    #    table_content = df.to_html(index=None)
    #    table_content = table_content.replace("", "")
    #    table_content = table_content.replace('class="dataframe"', "class='table table-striped'")
    #    table_content = table_content.replace('border="1"', "")
    # 'table_data': table_content
    return render(request, 'suspected.html', context=context)



def last_origin(request):
    dt = "7 de abril de 2020"
    file_name = "2020.04.07_confirmed_cases.csv"
    # read data

    df = pd.read_csv("api_covid19/files/"+file_name)
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
               'rango_de_edad': rango_de_edad, 'v_rango_de_edad' : v_rango_de_edad, 'file_name': file_name, 'dt': dt}
    return render(request, 'last_from.html', context=context)
