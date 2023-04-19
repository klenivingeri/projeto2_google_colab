# EXECUTAR CODIGO NO GOOGLE COLAB
import numpy as np
from scipy.stats import mode
import matplotlib.pyplot as plt

arq = open('ArquivoDadosProjeto.csv', 'r')

data = []
precip = []
maxima = []
minima = []
horas_insol = []
temp_media = []
um_relativa = []
vel_vento = []
dados_filtrados = []

# Leitura do arquivo e armazenamento em listas de listas/tuplas
for linhas in arq:
    valores = linhas.split(';')
    data.append((valores[0]))
    precip.append((valores[1]))
    maxima.append((valores[2]))
    minima.append((valores[3]))
    horas_insol.append((valores[4]))
    temp_media.append((valores[5]))
    um_relativa.append((valores[6]))
    vel_vento.append((valores[7]))
arq.close()

# a. Qual é o mês mais chuvoso em todo esse período? Isto é, o mês/ano com maior
# volume acumulado de chuva, considerando todos os dados do arquivo? Utilize 
# obrigatoriamente um dicionário.
def periodoChuvoso():
  print('\n\nAtividade a. ---------------------------------------------------------')
  acumulado_chuva = {}
  mes_mais_chuvoso = 0
  for i in range(1, len(data)):
    mes_ano = data[i][-7:]
    precipitacao = float(precip[i])
    if mes_ano in acumulado_chuva:
        acumulado_chuva[mes_ano] += precipitacao
    else:
        acumulado_chuva[mes_ano] = precipitacao

  for i, chuva in enumerate(acumulado_chuva):
    if acumulado_chuva[chuva] > mes_mais_chuvoso:
      mes_mais_chuvoso = acumulado_chuva[chuva]
  print(f"O perio mais chuvoso foi no mes  {chuva} com {mes_mais_chuvoso:.2f} de precipitação")

periodoChuvoso()

# b. Qual a média e a moda da temperatura mínima, umidade do ar e velocidade do vento
# no mês de agosto (auge do inverno) nos últimos 10 anos (2006 a 2016)? Escreva as
# informações pedidas para cada mês de agosto (agosto/2006, agosto/2007, ...agosto/2016) 
# e, de forma geral, que engloba todos os meses de agosto desse período de 10 anos.
def mediaModa():
  print('\n\nAtividade b. ---------------------------------------------------------')
  dados = {}
  for i in range(1, len(data)):
    dia = int(data[i][:2])
    mes = int(data[i][3:5])
    ano = int(data[i][-4:])

    # Armazena os dados no dicionário, agrupados por ano e mês
    if ano not in dados:
      dados[ano] = {}
    if mes not in dados[ano]:
      min = float(minima[i])
      rel = float(um_relativa[i])
      vel = float(vel_vento[i])
      dados[ano][mes] = []
      dados[ano][mes].append((min,rel,vel))

  for ano in range(2006, 2017):
    if ano not in dados:
      continue
    if 8 not in dados[ano]:
      if ano == 2016:
        print(f"\nAgosto/{ano}:")
        print('Não temos dados de 2016')
      continue

    dados_agosto = dados[ano][8]
    temperatura_min = [x[0] for x in dados_agosto]
    umidade_ar = [x[1] for x in dados_agosto]
    velocidade_vento = [x[2] for x in dados_agosto]

    print(f"\nAgosto/{ano}:")
    print(f"Média temperatura mínima: {np.mean(temperatura_min):.2f} °C")
    print(f"Moda temperatura mínima: {np.round(mode(temperatura_min)[0], 2)} °C")
    print(f"Média umidade do ar: {np.mean(umidade_ar):.2f} %")
    print(f"Moda umidade do ar: {np.round(mode(umidade_ar)[0], 2)} %")
    print(f"Média velocidade do vento: {np.mean(velocidade_vento):.2f} m/s")
    print(f"Moda velocidade do vento: {np.round(mode(velocidade_vento)[0], 2)} m/s")

  # Calcula a média e a moda para todos os meses de agosto nos últimos 10 anos
  temperaturaMin = []
  umidadeAr = []
  velocidadeVento = []
  for ano in range(2006, 2017):
    if ano not in dados:
        continue
    if 8 not in dados[ano]:
        continue
    dadosAgosto = dados[ano][8]
    temperaturaMin += [x[0] for x in dadosAgosto]
    umidadeAr += [x[1] for x in dadosAgosto]
    velocidadeVento += [x[2] for x in dadosAgosto]
  print("\nMédias e modas para todos os meses de agosto:")
  print(f"Média temperatura mínima: {np.mean(temperaturaMin):.2f}")
  print(f"Moda temperatura mínima: {np.round(mode(temperaturaMin)[0], 2)} °C")
  print(f"Média umidade do ar: {np.mean(umidadeAr):.2f} %")
  print(f"Moda umidade do ar: {np.round(mode(umidadeAr)[0], 2)} %")
  print(f"Média velocidade do vento: {np.mean(velocidadeVento):.2f} m/s")
  print(f"Moda velocidade do vento: {np.round(mode(velocidadeVento)[0], 2)} m/s")

mediaModa()

# c) Qual é a década mais chuvosa, isto é, a que possui maior média de chuva acumulada por ano?
# Para calcular isso, divida o volume de chuva da década pela quantidade de anos (lembre-se que 
# a última década só tem 6 anos - 2011 a 2016). Para realizar esse processamento, use as 
# estruturas de dados que você julgar necessário, tanto em tipo quanto em quantidade.
def mediaDecada():
  print('\n\nAtividade c. ---------------------------------------------------------')
  decadas = {}
  precipDecada = {}
  contaPrecip = 0
  anoDifAnterior = 0
  decadaAtaul = 0
  # Percorre todos os anos de 1961 a 2016
  for i in range(1, len(data)):
    ano = int(data[i][-4:])
    if ano != anoDifAnterior:
      contaPrecip = 0
      anoDifAnterior = ano
      # Identifica a década correspondente
      decada = str(((ano-1) // 10) * 10 +1)
      decadaAtaul = decada
      # Incrementa o valor correspondente da década no dicionário
      if decada in decadas:
        decadas[decada] += 1
      else:
        decadas[decada] = 1
    contaPrecip += float(precip[i])
    precipDecada[decadaAtaul] = contaPrecip

  decada_mais_chovosa = ''
  media_guardada = 0
  medias = []
  for chave, valor in decadas.items():
    media = precipDecada[chave] / valor

    if media > media_guardada:
        decada_mais_chovosa = "O ano de " + chave + " foi o ano mais chuvoso, com a média de precipitação " + str(round(media, 2))
        media_guardada = media
    medias.append(media)
  print(decada_mais_chovosa)

  # d) Além disso, você deve gerar um gráfico de barras com as médias acumuladas
  # por década. Não esqueça de rotular os eixos e usar legendas para deixar o seu
  # gráfico informativo e bem elaborado.
  print('\n\nAtividade d. ---------------------------------------------------------')

  x = list(decadas.keys())
  y = medias
  plt.bar(x, y)
  plt.xlabel('Década')
  plt.ylabel('Média acumulada de precipitação (mm)')
  plt.title('Médias acumuladas de precipitação por década')
  plt.show()

mediaDecada()


