import urllib

import PyPDF2
import pandas
import requests
import camelot.io as camelot
import pandas as pd
import glob
import json
import os
import re
import warnings
from datetime import datetime
from bs4 import BeautifulSoup
import zipfile


def downloadFile(url, filename, location='files/'):
    """
    Download file from given {url} and store file in disk
    Arguments:
        url -- File to download
        filename -- Name of the file to store in disk without .pdf extension
    """
#    url = url
    r = requests.get(url, allow_redirects=False, stream=True) #,
    success = r.status_code == requests.codes.ok

    if success:
        with open(f'api_covid19/{location}{filename}', 'wb') as f:
            f.write(r.content)
    else:
        warnings.warn(f"********", FutureWarning)
        warnings.warn(url + ' file not found', FutureWarning)

    return success

def getPagesNumber(filename):
    """
    Read PDF file and return number of pages
    Arguments:
        filename -- PDF to read without .pdf extension
    Return:
        Number of PDF pages
    """
    file = open(f'api_covid19/files/{filename}.pdf', 'rb')
    file_reader = PyPDF2.PdfFileReader(file)

    return file_reader.numPages;

def generateCSV(filename):
    """
    Read PDF files and then create a CSV equivalent.
    Arguments:
        filename -- PDF to read without .pdf extension
    """
    print(".", end='')
    # Get path and number of pages
    n_pages = getPagesNumber(filename)
    file_path = f'api_covid19/files/{filename}.pdf'

    # Convert PDF to CSV
    print(".", end='')
    tables = camelot.read_pdf(file_path, pages=f'1-{n_pages}', split_text=True)
    print(".", end='')
    tables.export(f'api_covid19/files/intermediate_{filename}.csv', f='csv', compress=False)
    print(".", end='')

    # Merge generated CSV files into just one
    all_filenames = [i for i in sorted(glob.glob(f'api_covid19/files/intermediate_{filename}*.csv'))]
    combined_csv = pd.read_csv(all_filenames[0])
    print(".", end='')

    for idx, f in enumerate(all_filenames):
        if idx > 0:
            df = pd.read_csv(f, header=None)
            df.columns = combined_csv.columns
            combined_csv = combined_csv.append(df)

    print(".", end='')
    combined_csv.to_csv(f'api_covid19/static/files/{filename}.csv', index=False, encoding='utf-8-sig')

    # Finally remove intermediate CSV files
    for f in all_filenames:
        os.remove(f)


def getPDFLinks():
    """
    Scrap https://www.gob.mx/ website to get last links of the thecnical documents.
    Return:
        Dictionary with PDF links of confirmed and positives cases
    """
    url = 'https://www.gob.mx/salud/documentos/coronavirus-covid-19-comunicado-tecnico-diario-238449'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = {}

    html_table = soup.find('div', class_='table-responsive')

    for a in html_table.find_all('a'):
        if 'positivos' in a['href']:
            links['confirmed_cases'] = 'https://www.gob.mx/' + a['href']
        elif 'sospechosos' in a['href']:
            links['suspected_cases'] = 'https://www.gob.mx/' + a['href']

    return links


def proc_download(url, filename, location='files/'):
    if os.path.exists(f'api_covid19/{location}{filename}'):
        print(filename + " ya existía")
    else:
        downloadFile(url=url, filename=filename, location=location)
        print(filename + " descargado")


def run_prev():
    print("Iniciando")
    pdf_links = getPDFLinks()
     # Extract date from document URL
    report_date = re.findall('[0-9]*\.[0-9]*\.[0-9]*', pdf_links['confirmed_cases'])[0]

    # Documents filenames
    cc_filename = f'{report_date}_confirmed_cases' # Confirmed cases filename
    sc_filename = f'{report_date}_suspected_cases' # Suspected cases filename
    print(pdf_links)

    proc_download(pdf_links['confirmed_cases'], cc_filename+'.pdf')
    proc_download(pdf_links['suspected_cases'], sc_filename+'.pdf')

    if os.path.exists(f'api_covid19/static/files/{cc_filename}.csv'):
        print(cc_filename + ".csv ya existía")
    else:
        generateCSV(cc_filename)
        print(cc_filename + ".csv generado")

    # if os.path.exists(f'api_covid19/static/files/{sc_filename}.csv'):
    #     print(sc_filename + ".csv ya existía")
    # else:
    #     generateCSV(sc_filename)
    #     print(sc_filename + ".csv generado")

def run():
    print("Iniciando")

    to_path = 'static/files/'
    ecdc_url = f"https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    ecdc_filename = "ecdc_cases_" + datetime.today().strftime("%Y.%m.%d") + '.csv'
    # proc_download(ecdc_url, ecdc_filename, to_path)
    # u2 = urllib.request.urlopen(ecdc_url)
    # for lines in u2.readlines():
    #     print(lines)
    if os.path.exists(f'api_covid19/{to_path}{ecdc_filename}'):
        print(f'{ecdc_filename} ya existía')
    else:
        df = pd.read_csv(ecdc_url)
        df.to_csv('api_covid19/' + to_path + ecdc_filename)
        print("Archivo " + ecdc_filename + " guardado.")

    datos_abiertos = 'api_covid19/' + to_path + datetime.today().strftime("%y%m%d") + 'COVID19MEXICO.csv'
    if os.path.exists(datos_abiertos):
        print(f'{datos_abiertos} ya existía')
    else:
        da_url = f"http://187.191.75.115/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip"
        da_filename = "tmp_datos_abiertos_covid19.zip"
        proc_download(da_url, da_filename, to_path)

        with zipfile.ZipFile('api_covid19/' + to_path + da_filename, 'r') as zip_ref:
            da_file = zip_ref.namelist()[0];
            zip_ref.extractall('api_covid19/' + to_path)

        datos_abiertos = 'api_covid19/' + to_path + da_file
        print("Datos Abiertos File = " + datos_abiertos)
        os.remove('api_covid19/' + to_path + da_filename)

        import sqlite3
        conn = sqlite3.connect("covid19mx.db")
        df = pandas.read_csv(datos_abiertos, encoding = "latin")
        df.to_sql("datos_abiertos_MX", conn, if_exists='replace', index='id')
        print("Datos Abiertos copiados a SQLLITE")
        conn.close()

    run_prev()

if __name__ == '__main__':
    run()