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

    dados.append({
        "Apelido": jogador.get('apelido', 'Desconhecido'),
        "Clube": clube_nome,
        "Posição": posicao_nome,
        "Preço (C$)": jogador.get('preco_num', 0),
        "Média Pontuação": jogador.get('media_num', 0),
        "Última Pontuação": jogador.get('pontos_num', 0),
        "Mínimo para Valorizar": jogador.get('minimo_para_valorizar', 0),
        "Variação de Preço": jogador.get('variacao_num', 0)
    })

df = pd.DataFrame(dados)

# Ordenação e filtragem dos jogadores
df = df.dropna(subset=["Preço (C$)"])
df = df.sort_values(by=["Média Pontuação", "Mínimo para Valorizar"], ascending=[False, True])

# Entrada do usuário para orçamento
saldo = float(input("Digite o número de cartoletas disponíveis: "))

def criar_time(df, saldo):
    while True:
        time = {
            "Goleiro": random.choice(df[df["Posição"] == "Goleiro"].head(5).to_dict('records')),
            "Zagueiros": random.sample(df[df["Posição"] == "Zagueiro"].head(10).to_dict('records'), 2),
            "Laterais": random.sample(df[df["Posição"] == "Lateral"].head(10).to_dict('records'), 2),
            "Meias": random.sample(df[df["Posição"] == "Meia"].head(15).to_dict('records'), 3),
            "Atacantes": random.sample(df[df["Posição"] == "Atacante"].head(10).to_dict('records'), 2),
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
                dados_saida.append([f"Time {i}", posicao, jogador["Apelido"], jogador["Preço (C$)"]])
        else:
            dados_saida.append([f"Time {i}", posicao, jogadores["Apelido"], jogadores["Preço (C$)"]])

saida_df = pd.DataFrame(dados_saida, columns=["Time", "Posição", "Apelido", "Preço (C$)"])

# Salvar os times recomendados em Excel
saida_df.to_excel("times_recomendados.xlsx", index=False)
print("Arquivo 'times_recomendados.xlsx' gerado com sucesso!")
