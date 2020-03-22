import PyPDF2
import requests
import camelot
import pandas as pd
import glob
import json
import os
import re
import warnings
from datetime import datetime
from bs4 import BeautifulSoup

def downloadPDF(url, filename):
    """
    Download file from given {url} and store file in disk
    Arguments:
        url -- File to download
        filename -- Name of the file to store in disk without .pdf extension
    """
    url = url
    r = requests.get(url, stream=True, allow_redirects=False)
    success = r.status_code == requests.codes.ok

    if success:
        with open(f'api_covid19/files/{filename}.pdf', 'wb') as f:
            f.write(r.content)
    else:
        warnings.warn(f"********", FutureWarning)
        warnings.warn(f'{url} file not found', FutureWarning)

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

def parsePDF(filename):
    """
    Read PDF file and then create a CSV equivalent
    Arguments:
        filename -- PDF to read without .pdf extension
    """
    print(f'Parsing file... {filename}')

    # Get path and number of pages
    n_pages = getPagesNumber(filename)
    file_path = f'api_covid19/files/{filename}.pdf'

    # Convert PDF to CSV
    tables = camelot.read_pdf(file_path, pages=f'1-{n_pages}', split_text=True)
    tables.export(f'api_covid19/files/intermediate_{filename}.csv', f='csv', compress=False)

    # Merge generated CSV files into just one
    all_filenames = [i for i in sorted(glob.glob(f'api_covid19/files/intermediate_{filename}*.csv'))]
    combined_csv = pd.read_csv(all_filenames[0])

    for idx, f in enumerate(all_filenames):
        if idx > 0:
            df = pd.read_csv(f, header=None)
            df.columns = combined_csv.columns
            combined_csv = combined_csv.append(df)

    combined_csv.to_csv(f'api_covid19/files/{filename}.csv', index=False, encoding='utf-8-sig')

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

def run():
    pdf_links = getPDFLinks()
     # Extract date from document URL
    report_date = re.findall('[0-9]*\.[0-9]*\.[0-9]*', pdf_links['confirmed_cases'])[0]

    # Documents filenames
    confirmed_cases_filename = f'{report_date}_confirmed_cases'
    suspected_cases_filename = f'{report_date}_suspected_cases'

    downloadPDF(url=pdf_links['confirmed_cases'],
                filename=confirmed_cases_filename)
    parsePDF(confirmed_cases_filename)

    downloadPDF(url=pdf_links['suspected_cases'],
                filename=suspected_cases_filename)
    parsePDF(suspected_cases_filename)
