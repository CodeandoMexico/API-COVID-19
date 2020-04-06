from django.shortcuts import render
import pandas as pd


def index(request):
    """ view function for sales app """
    file_name = "2020.04.05_confirmed_cases.csv"
    # read data

    df = pd.read_csv("api_covid19/files/"+file_name)
    rs = df.groupby("Estado")["Procedencia"].count().reset_index() \
                      .sort_values('Procedencia', ascending=False) \
                      .set_index('Estado')
    print("**simple group by *********")
    print(rs)
#    rs = estados["Procedencia"].agg("count")
        # .reset_index(name='count') \
        #                      .sort_values(['count'], ascending=False)
#    print(rs)
    categories = list(rs.index)
    values = list(rs.values)
    print(values)
    for i, v in enumerate(values):
        # print(i)
        # print(values[i])
        # print(values[i].item())
        values[i] = values[i][0]


    table_content = df.to_html(index=None)
    table_content = table_content.replace("", "")
    table_content = table_content.replace('class="dataframe"', "class='table table-striped'")
    table_content = table_content.replace('border="1"', "")

    context = {"categories": categories, 'values': values, 'table_data': table_content, 'file_name': file_name}
    return render(request, 'index.html', context=context)