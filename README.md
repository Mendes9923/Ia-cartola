# Cartola FC - Gerador de Times

Este projeto unifica a coleta de dados do Cartola FC e a geração de times otimizados com base em métricas de desempenho e orçamento disponível.

## 📌 Funcionalidades
- Obtém dados dos jogadores diretamente da API do Cartola FC.
- Processa e organiza os dados dos jogadores, incluindo preços, médias de pontuação e valorização.
- Gera três times aleatórios respeitando o saldo de cartoletas definido pelo usuário.
- Salva os times recomendados em um arquivo Excel (`times_recomendados.xlsx`).

  
#Exista dois tipo de analise 

## 🚀 Tipo 1
1. Certifique-se de ter o Python instalado.
2. Instale as dependências necessárias com:
   ```bash
   pip install requests pandas openpyxl
   ```
3. Execute o script:
   ```bash
   python meu_cartola.py
   ```
4. Atraves de API vai buscar as iinformações de todos os jogadores.
5. O arquivo `jogadores_cartola.xlsx` será gerado um arquivoi com todos os jogadores.
6. Execute o script:
   ```bash
   python ia_cartola.py
   ```
Insira o número de cartoletas disponíveis quando solicitado.
7. O arquivo `times_recomendados.xlsx` será gerado com os três times criados.


## 🚀 2 opção
1. Certifique-se de ter o Python instalado.
2. Instale as dependências necessárias com:
   ```bash
   pip install requests pandas openpyxl
   ```
3. Execute o script:
   ```bash
   python ia_cartolaV1.py
   ```
4. Insira o número de cartoletas disponíveis quando solicitado.
5. O arquivo `times_recomendados.xlsx` será gerado com os três times criados.

## 🛠 Tecnologias Utilizadas
- Python
- Pandas
- Requests
- API do Cartola FC

## 📄 Licença
Este projeto é livre para uso e modificação.

---
⚽ Boa sorte no Cartola FC! Se precisar de melhorias, contribua com sugestões! 🚀
---



