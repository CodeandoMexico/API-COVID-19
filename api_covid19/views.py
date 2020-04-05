from django.shortcuts import render
import pandas as pd


def index(request):
    """ view function for sales app """
    file_name = "2020.04.03_confirmed_cases.csv"
    # read data

    df = pd.read_csv("api_covid19/files/"+file_name)
    rs = df.groupby("Estado")["Procedencia"].agg("count")
    categories = list(rs.index)
    values = list(rs.values)

    table_content = df.to_html(index=None)

    table_content = table_content.replace("", "")
    table_content = table_content.replace('class="dataframe"', "class='table table-striped'")
    table_content = table_content.replace('border="1"', "")

    context = {"categories": categories, 'values': values, 'table_data': table_content, 'file_name': file_name}
    return render(request, 'index.html', context=context)