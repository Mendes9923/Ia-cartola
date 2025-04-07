import requests
import pandas as pd

# URL para pegar todos os jogadores do mercado
url = "https://api.cartolafc.globo.com/atletas/mercado"

# Faz a requisição para a API
response = requests.get(url)
dados_mercado = response.json()

# Acessa os dados dos jogadores, clubes e posições
jogadores = dados_mercado['atletas']
clubes = dados_mercado['clubes']
posicoes = dados_mercado['posicoes']

# Lista para armazenar os dados
dados = []

# Itera sobre os jogadores e coleta as informações
for jogador in jogadores:
    clube_id = jogador.get('clube_id')
    clube_nome = clubes.get(str(clube_id), {}).get('nome', 'Desconhecido')
    
    posicao_id = jogador.get('posicao_id')
    posicao_nome = posicoes.get(str(posicao_id), {}).get('nome', 'Desconhecido')
    
    # Estatísticas do scout
    scout = jogador.get('scout', {})
    desarmes = scout.get('DS', 0)
    faltas_cometidas = scout.get('FC', 0)
    finalizacoes_defendidas = scout.get('FD', 0)
    finalizacoes_fora = scout.get('FF', 0)
    
    # Dados do gato_mestre
    gato_mestre = jogador.get('gato_mestre', {})
    media_pontos_mandante = gato_mestre.get('media_pontos_mandante', 'N/A')
    media_pontos_visitante = gato_mestre.get('media_pontos_visitante', 'N/A')
    media_minutos_jogados = gato_mestre.get('media_minutos_jogados', 'N/A')
    
    # Mínimo para valorizar
    minimo_valorizar = jogador.get('minimo_para_valorizar', 'N/A')
    
    dados.append({
        "Nome": jogador.get('nome', 'Desconhecido'),
        "Apelido": jogador.get('apelido', 'Desconhecido'),
        "Clube": clube_nome,
        "Posição": posicao_nome,
        "Preço (C$)": jogador.get('preco_num', 0),
        "Média Pontuação": jogador.get('media_num', 0),
        "Última Pontuação": jogador.get('pontos_num', 0),
        "Mínimo para Valorizar": minimo_valorizar,
        "Variação de Preço": jogador.get('variacao_num', 0),
        "Entrou em Campo": jogador.get('entrou_em_campo', False),
        "Desarmes (DS)": desarmes,
        "Faltas Cometidas (FC)": faltas_cometidas,
        "Finalizações Defendidas (FD)": finalizacoes_defendidas,
        "Finalizações Fora (FF)": finalizacoes_fora,
        "Média Pontos Mandante": media_pontos_mandante,
        "Média Pontos Visitante": media_pontos_visitante,
        "Média Minutos Jogados": media_minutos_jogados
    })

# Converte para um DataFrame do Pandas
df = pd.DataFrame(dados)

# Salva os dados em um arquivo Excel
arquivo_excel = "jogadores_cartola_atualizado.xlsx"
df.to_excel(arquivo_excel, index=False)

print(f"Arquivo '{arquivo_excel}' gerado com sucesso! 🎉")