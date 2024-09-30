import numpy as np
import pandas as pd
import yfinance as yf 
import datetime as dt
import plotly.express as px
import matplotlib.pyplot as plt
import glob
import matplotlib.dates as mdates



dados_diarios = pd.read_csv('df_diario.csv')

now = dt.datetime.now()
dia_hoje = now.day    
data_format = now.strftime("%Y-%m-%d")
hora_minuto = now.strftime("%H:%M")



if dados_diarios['day'].min() != dia_hoje:
        dados_dia_anterior = dados_diarios.loc[dados_diarios['day'] == dados_diarios['day'].min(),:]
        dados_dia_anterior.to_csv('dados_dia_anterior.csv')
        dados_diarios = dados_diarios.loc[dados_diarios['day'] == dia_hoje,:]
    
    
brasil_tickers = ["BRBI11.SA","BBAS3.SA", "RAIZ4.SA", "BBSE3.SA", "VALE3.SA"] # defina aqui os tickers


for acao in brasil_tickers:
    caminho = 'dados_brutos/dados_'+ acao +'.csv'

    # Função para baixar dados do ticker selecionado com intervalo de 5 minutos
    def baixar_dados(ticker, start_date):
        data = yf.download(
            tickers=ticker,            
            start=start_date,           
            interval="5m"                                  
        )
        # start: Data de início no formato YYYY-MM-DD.
        # interval: Frequência dos dados (opções: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo).
        
        return data

    dados_diarios = baixar_dados(acao, data_format)
    dados_diarios = dados_diarios.loc[:,['Close','Volume']]
    
    dados_diarios.to_csv(caminho)


# Criando lista de arquivos CSV
caminho_dos_arquivos = 'dados_brutos/*.csv' 
arquivos_csv = glob.glob(caminho_dos_arquivos)

dfs = []

# Loop para ler e processar cada arquivo CSV
for arquivo in arquivos_csv:

    df = pd.read_csv(arquivo)
    
    nome_acao = arquivo.split('_')[-1].replace('.SA.csv', '')
    df['acao'] = nome_acao
    
    dfs.append(df)

# Concatenar dataframes
resultado = pd.concat(dfs, ignore_index=True)
resultado['Datetime'] = pd.to_datetime(resultado['Datetime'])
resultado['day'] = resultado['Datetime'].dt.day

resultado.to_csv('df_diario.csv', index=False)