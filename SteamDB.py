#!/usr/bin/env python
# coding: utf-8

# # STEAMDB - SALES

# ## WEBSCRAPING + CSV para o Big Query


import pandas as pd
from bs4 import BeautifulSoup
from google.cloud import bigquery

def parse_html(file_path):
    # Lê o arquivo HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Faz o parsing do conteúdo HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    return soup

def extract_data(soup):
    # Cria uma lista vazia para armazenar os dados
    data = []

    # Itera sobre cada linha da tabela HTML
    for row in soup.find_all('tr'):
        # Encontra os campos name, discount, price, rating e ends_in
        name = row.find('a', class_='b')
        discount = row.find('td', class_='price-discount-major')
        price = None
        for td in row.find_all('td'):
            if td.text.strip().startswith('R$'):
                price = td.text.strip()
                break
        rating = row.find('td', {'data-sort': lambda x: x is not None and '.' in x})
        ends_in = row.find('td', class_='timeago')

        # Encontra os campos started e release com base no campo ends_in
        if ends_in:
            started = ends_in.find_next_sibling('td', class_='timeago')
            if started:
                release = started.find_next_sibling('td', {'data-sort': True})
            else:
                release = None
        else:
            started = None
            release = None

        # Verifica se todos os campos necessários estão presentes
        if name and discount and price and rating and ends_in:
            # Extrai o texto de cada campo e armazena em variáveis
            name_text = name.text.strip() if name.text else ''
            discount_text = discount.text.strip() if discount.text else ''
            price_text = price
            rating_text = rating.text.strip() if rating.text else ''
            ends_in_text = ends_in.text.strip() if ends_in.text else ''
            started_text = started.text.strip() if started and started.text else ''
            release_text = release.text.strip() if release and release.text else ''

            # Adiciona os dados como um dicionário à lista
            data.append({
                'Name': name_text,
                '%': discount_text,
                'Price': price_text,
                'Rating': rating_text,
                'Ends in': ends_in_text,
                'Started': started_text,
                'Release': release_text
            })

    return data

def save_to_csv(data, csv_file_path):
    # Cria um DataFrame usando os dados coletados
    df = pd.DataFrame(data)

    # Salva o DataFrame em um arquivo CSV
    df.to_csv(csv_file_path, index=False)

def load_to_bigquery(csv_file_path, project_id, dataset_id, table_name):
    # Configura o cliente do BigQuery
    client = bigquery.Client()

    # Define os detalhes da tabela do BigQuery
    dataset_ref = client.dataset(dataset_id, project=project_id)
    table_ref = dataset_ref.table(table_name)

    # Define o esquema da tabela do BigQuery
    schema = [
        bigquery.SchemaField('Name', 'STRING'),
        bigquery.SchemaField('%', 'STRING'),
        bigquery.SchemaField('Price', 'STRING'),
        bigquery.SchemaField('Rating', 'STRING'),
        bigquery.SchemaField('Ends in', 'STRING'),
        bigquery.SchemaField('Started', 'STRING'),
        bigquery.SchemaField('Release', 'STRING')
    ]

    # Carrega o arquivo CSV para a tabela do BigQuery
    job_config = bigquery.LoadJobConfig(schema=schema, source_format=bigquery.SourceFormat.CSV)
    with open(csv_file_path, 'rb') as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()  # Aguarda a conclusão do job

    # Imprime a confirmação
    print('Dados carregados na tabela do BigQuery:', table_name)

# Caminho do arquivo baixado na minha máquina
file_path = r'C:\Users\Notbook I3\Downloads\Steam Summer Sale 2023 · BR · SteamDB.html'

# Parse do HTML
soup = parse_html(file_path)

# Extrair dados
data = extract_data(soup)

# Caminho do arquivo CSV para salvar os dados
csv_file_path = 'dados_steam_sale.csv'

# Salvar dados em CSV
save_to_csv(data, csv_file_path)

# Configuração do BigQuery
project_id = 'steamdb-beanalitics'
dataset_id = 'steamdb_sales'
table_name = 'steamdb_sales'

# Carregar dados para o BigQuery
load_to_bigquery(csv_file_path, project_id, dataset_id, table_name)


## ENVIAR DO BIG_QUERY PARA GOOGLE SHEETS


import pandas as pd
import gspread
from google.oauth2 import service_account
from google.cloud import bigquery

def run_bigquery_query(project_id, dataset_id, table_name):
    # Configuração do cliente BigQuery
    client_bq = bigquery.Client(project=project_id)
    table_ref = client_bq.dataset(dataset_id).table(table_name)

    # Executa uma consulta e obtém os resultados
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_name}`"
    query_job = client_bq.query(query)
    results = query_job.result()

    # Converte os resultados em um DataFrame do pandas
    df = pd.DataFrame(results.to_dataframe())

    return df

def upload_dataframe_to_google_sheets(df, credentials_file, spreadsheet_id, sheet_index=0):
    # Configuração das credenciais do Google Sheets
    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    credentials = credentials.with_scopes(['https://www.googleapis.com/auth/spreadsheets'])

    client_sheets = gspread.authorize(credentials)

    # Abre a planilha do Google Sheets
    spreadsheet = client_sheets.open_by_key(spreadsheet_id)

    # Seleciona a aba da planilha
    worksheet = spreadsheet.get_worksheet(sheet_index)

    # Limpa os dados existentes na planilha
    worksheet.clear()

    # Converte o DataFrame para uma lista de listas
    values = df.values.tolist()

    # Insere os novos dados na planilha
    worksheet.update(values)

    print('Dados enviados com sucesso para o Google Sheets!')

# Configuração do projeto do BigQuery
project_id = 'steamdb-beanalitics'
dataset_id = 'steamdb_sales'
table_name = 'steamdb_sales'

# Configuração do projeto do Google Sheets
credentials_file = 'steamdb-beanalitics-22915f5de0a0.json'
spreadsheet_id = '1ulcB7BD5VQXL4eGpyp2X9eZWwK8ltW_oRy4p-I0-AyU'

# Executa a consulta no BigQuery e obtém os resultados como DataFrame
df = run_bigquery_query(project_id, dataset_id, table_name)

# Envia o DataFrame para o Google Sheets
upload_dataframe_to_google_sheets(df, credentials_file, spreadsheet_id)


