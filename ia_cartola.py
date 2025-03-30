import pandas as pd
import random

# Caminho do arquivo de entrada
file_path = "jogadores_cartola.xlsx"

# Carregar os dados
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name="Sheet1")

# Converter colunas numéricas
cols_numericas = ["Preço (C$)", "Mínimo para Valorizar", "Variação de Preço", "Média Pontuação", "Última Pontuação", "Média Pontos Mandante", "Média Pontos Visitante"]
for col in cols_numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remover jogadores sem preço definido
df = df.dropna(subset=["Preço (C$)"])

# Filtrar os melhores jogadores para pontuação e valorização
df = df.sort_values(by=["Média Pontuação", "Mínimo para Valorizar"], ascending=[False, True])

# Solicitar o valor de cartoletas disponíveis
saldo = float(input("Digite o número de cartoletas disponíveis: "))

# Função para criar um time respeitando o orçamento
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

# Gerar três times diferentes
times = [criar_time(df, saldo) for _ in range(3)]

# Criar DataFrame de saída
dados_saida = []
for i, time in enumerate(times, 1):
    for posicao, jogadores in time.items():
        if isinstance(jogadores, list):
            for jogador in jogadores:
                dados_saida.append([f"Time {i}", posicao, jogador["Nome"], jogador["Preço (C$)"]])
        else:
            dados_saida.append([f"Time {i}", posicao, jogadores["Nome"], jogadores["Preço (C$)"]])

saida_df = pd.DataFrame(dados_saida, columns=["Time", "Posição", "Nome", "Preço (C$)"])

# Salvar em Excel
saida_df.to_excel("times_recomendados.xlsx", index=False)
print("Arquivo 'times_recomendados.xlsx' gerado com sucesso!")
