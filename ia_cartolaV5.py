import requests
import pandas as pd
import random

# URL da API do Cartola FC
url = "https://api.cartolafc.globo.com/atletas/mercado"
response = requests.get(url)
dados_mercado = response.json()

# Processamento dos dados dos jogadores
jogadores = dados_mercado['atletas']
clubes = dados_mercado['clubes']
posicoes = dados_mercado['posicoes']

dados = []
for jogador in jogadores:
    clube_id = jogador.get('clube_id')
    clube_nome = clubes.get(str(clube_id), {}).get('nome', 'Desconhecido')
    posicao_id = jogador.get('posicao_id')
    posicao_nome = posicoes.get(str(posicao_id), {}).get('nome', 'Desconhecido')
    
    scout = jogador.get('scout', {})
    desarmes = scout.get('DS', 0)
    finalizacoes_defendidas = scout.get('FD', 0)
    finalizacoes_fora = scout.get('FF', 0)
    faltas_cometidas = scout.get('FC', 0)
    
    dados.append({
        "Apelido": jogador.get('apelido', 'Desconhecido'),
        "Clube": clube_nome,
        "Posição": posicao_nome,
        "Preço (C$)": jogador.get('preco_num', 0),
        "Média Pontuação": jogador.get('media_num', 0),
        "Última Pontuação": jogador.get('pontos_num', 0),
        "Mínimo para Valorizar": jogador.get('minimo_para_valorizar', 0),
        "Variação de Preço": jogador.get('variacao_num', 0),
        "Desarmes (DS)": desarmes,
        "Finalizações Defendidas (FD)": finalizacoes_defendidas,
        "Finalizações Fora (FF)": finalizacoes_fora,
        "Faltas Cometidas (FC)": faltas_cometidas
    })

df = pd.DataFrame(dados)

# Filtrar e ordenar jogadores considerando múltiplas métricas
# Critérios: Menos faltas cometidas, mais desarmes, mais finalizações ao gol e para fora, melhores pontuações na média e maior chance de valorização
df = df.sort_values(by=["Média Pontuação", "Desarmes (DS)", "Finalizações Defendidas (FD)", "Finalizações Fora (FF)", "Variação de Preço"], ascending=[False, False, False, False, False])
df = df[df["Faltas Cometidas (FC)"] == 0]  # Excluir jogadores com faltas cometidas

# Entrada do usuário para orçamento
saldo = float(input("Digite o número de cartoletas disponíveis: "))

def criar_time(df, saldo):
    while True:
        time = {
            "Goleiro": random.choice(df[df["Posição"] == "Goleiro"].head(5).to_dict('records')),
            "Zagueiros": random.sample(df[df["Posição"] == "Zagueiro"].head(10).to_dict('records'), 2),
            "Laterais": random.sample(df[df["Posição"] == "Lateral"].head(10).to_dict('records'), 2),
            "Meias": random.sample(df[df["Posição"] == "Meia"].head(15).to_dict('records'), 3),
            "Atacantes": random.sample(df[df["Posição"] == "Atacante"].head(10).to_dict('records'), 3),
            "Técnico": random.choice(df[df["Posição"] == "Técnico"].head(5).to_dict('records'))
        }
        
        custo_total = (time["Goleiro"]["Preço (C$)"] + sum(j["Preço (C$)"] for j in time["Zagueiros"]) +
                       sum(j["Preço (C$)"] for j in time["Laterais"]) + sum(j["Preço (C$)"] for j in time["Meias"]) +
                       sum(j["Preço (C$)"] for j in time["Atacantes"]) + time["Técnico"]["Preço (C$)"])
        
        if custo_total <= saldo:
            return time

# Gerar três times
times = [criar_time(df, saldo) for _ in range(3)]

dados_saida = []
for i, time in enumerate(times, 1):
    for posicao, jogadores in time.items():
        if isinstance(jogadores, list):
            for jogador in jogadores:
                dados_saida.append([f"Time {i}", posicao, jogador["Apelido"], jogador["Preço (C$)"], jogador["Média Pontuação"], jogador["Última Pontuação"]])
        else:
            dados_saida.append([f"Time {i}", posicao, jogadores["Apelido"], jogadores["Preço (C$)"], jogadores["Média Pontuação"], jogadores["Última Pontuação"]])

saida_df = pd.DataFrame(dados_saida, columns=["Time", "Posição", "Apelido", "Preço (C$)", "Média Pontuação", "Última Pontuação"])

# Salvar os times recomendados em Excel
saida_df.to_excel("times_recomendados_v5.xlsx", index=False)
print("Arquivo 'times_recomendados_v5.xlsx' gerado com sucesso!")