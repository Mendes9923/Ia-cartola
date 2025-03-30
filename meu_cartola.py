import requests
import pandas as pd

# URL para pegar todos os jogadores do mercado
url = "https://api.cartolafc.globo.com/atletas/mercado"

# Faz a requisição para a API
response = requests.get(url)
dados_mercado = response.json()  # Pega a resposta no formato JSON

# Acessa os dados dos jogadores, clubes e posições
jogadores = dados_mercado['atletas']
clubes = dados_mercado['clubes']  # Dicionário de clubes
posicoes = dados_mercado['posicoes']  # Dicionário de posições

# Inspeciona os dados de um jogador para entender a estrutura
print(jogadores[0])  # Mostra o primeiro jogador para inspecionar a estrutura

# Cria lista para armazenar os dados
dados = []

# Itera sobre os jogadores e coleta as informações
for jogador in jogadores:
    clube_id = jogador.get('clube_id')  # Obtém o ID do clube
    clube_nome = clubes.get(str(clube_id), {}).get('nome', 'Desconhecido')  # Nome do clube
    
    posicao_id = jogador.get('posicao_id')  # Obtém o ID da posição
    posicao_nome = posicoes.get(str(posicao_id), {}).get('nome', 'Desconhecido')  # Nome da posição

    preco = jogador.get('preco_num', 0)  # Preço correto
    media = jogador.get('media_num', 0)  # Média de pontos
    pontos_num = jogador.get('pontos_num', 0)  # Última pontuação
    minimo_valorizar = jogador.get('minimo_para_valorizar', 'Não disponível')  # Mínimo para valorizar
    variacao = jogador.get('variacao_num', 0)  # Variação de preço
    entrou_em_campo = jogador.get('entrou_em_campo', False)  # Se entrou em campo

    # Informações sobre minutos jogados e médias
    media_pontos_mandante = jogador.get('media_pontos_mandante', 'Não disponível')
    media_pontos_visitante = jogador.get('media_pontos_visitante', 'Não disponível')
    media_minutos_jogados = jogador.get('media_minutos_jogados', 'Não disponível')
    minutos_jogados = jogador.get('minutos_jogados', 'Não disponível')

    dados.append({
        "Nome": jogador.get('nome', 'Desconhecido'),
        "Apelido": jogador.get('apelido', 'Desconhecido'),
        "Clube": clube_nome,
        "Posição": posicao_nome,
        "Preço (C$)": preco,
        "Média Pontuação": media,
        "Última Pontuação": pontos_num,
        "Mínimo para Valorizar": minimo_valorizar,
        "Variação de Preço": variacao,
        "Entrou em Campo": entrou_em_campo,
        "Média Pontos Mandante": media_pontos_mandante,
        "Média Pontos Visitante": media_pontos_visitante,
        "Média Minutos Jogados": media_minutos_jogados,
        "Minutos Jogados": minutos_jogados
    })

# Converte para um DataFrame do Pandas
df = pd.DataFrame(dados)

# Salva os dados em um arquivo Excel
arquivo_excel = "jogadores_cartola.xlsx"
df.to_excel(arquivo_excel, index=False)

print(f"Arquivo '{arquivo_excel}' gerado com sucesso! 🎉")
