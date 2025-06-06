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
    distancia= abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo)

    print("\nMEDIDAS DE POSIÇÃO")
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância entre a média e mediana {distancia:.3f}')

#   MEDIDAS DE POSOÇÃO
#   QUARTIL
    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull')
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull')
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull')
    
    print("\nMEDIDAS DE POSIÇÃO")
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

#   ROUBO MAIS E ROUBO MENOS
#   MENOR ROUBOS
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] <q1]

#   MAIOR ROUBOS
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] >q3]

    print('\nMunicípio com Menores números de Roubos')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))

    print('\nMunicípios com Maior números de Roubos')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

#   INDENTIFICANDO OUTLIERS
    #   IQR
    iqr = q3 - q1

    limite_superior = q3 + (1.5 * iqr)
    limite_inferio = q1 - (1.5 * iqr)

    print("\nLimites - Medidas de Posição")
    print(f'Limites inferior: {limite_inferio}')
    print(f'Limites superior: {limite_superior}')

#   DESCOBRINDO oUTLIERS
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferio]

#   OUTLIERS INFERIORES
    print(f'\nOutliers Inferiores')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não há outliers inferiores')
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))

#   OUTLIERS SUPERIORES
    print(f'\nOutliers Superiores')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não há outliers Superiores')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))

except Exception as e:
    print(f"Errdo de processamento de dados: {e}")
    exit()