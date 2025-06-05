from utils import limpar_nome_municipio
import pandas as pd
import numpy as np

try:
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_ocorrencia = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencia.head())
    for i in range(2):
        df_ocorrencia['munic'] = df_ocorrencia['munic'].apply(limpar_nome_municipio)
    #   DELIMITANDO VARIÁVEIS
    df_ocorrencia = df_ocorrencia[['munic', 'roubo_veiculo']]
#   TOTALIZANDO
    df_roubo_veiculo = df_ocorrencia.groupby('munic').sum(['roubo_veiculo']).reset_index()
    print(df_roubo_veiculo.to_string())
except Exception as e:
    print(f"Errdo de conexão: {e}")
    exit()

#   INICIALIZANDO ANÁLISE

try:
    print('Obtendo informações sobre padrão de roubos de veículos...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])
    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia= abs(media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo 
      
    print(30*'-')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(distancia)

except Exception as e:
    print(f"Errdo de conexão: {e}")
    exit()