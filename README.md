# bootcamp-ds-4ed
Repositório do Grupo 1 do Bootcamp de Introdução à Data Science - Edição 2025/2

# Bootcamp de Introdução a Data Science: PROJETO FINOR

## Briefing Técnico

### Problemática Inicial

Os modelos de *index tracking* buscam reproduzir o comportamento de índices de ações com um número de ações inferior ao do índice original, simplificando a composição do portfólio e, consequentemente, o custo de manutenção do portfólio.

### Objetivo

O objetivo desse projeto é desenvolver um modelo de *index tracking* para os índices S&P100 e IBOV.

### Motivação

Os índices de mercado (por exemplo, S&P500) são compostos por ações individuais e representam termômetros dos mercados de ações. Fundos de investimento passivo visam replicar o desempenho de um índice de mercado ou de um segmento específico do mercado.

### Dados

Os participantes devem buscar os dados históricos dos últimos 7 anos dos índices S&P 100 e IBOVESPA para serem utilizados como inputs. [cite: 8] [cite_start]Os dados podem ser encontrados no Yahoo Finance e outros locais de interesse do grupo.

### Index tracking (IT)

* IT consiste em uma estratégia de replicar um índice de mercado utilizando um número menor de ações. 
* IT apresenta menores custos e, por ter menos ativos, fornece uma carteira de ações mais simples de ser gerida. 
* IT no formato de problema de otimização pode ser incrementado com restrições de negócio.

### Etapas

A implementação do modelo de otimização deve ser realizada em Python, podendo ser utilizadas API's de Python de solvers como Gurobi ou de solvers open-source. 

1.  **Importar os dados**: a partir de arquivos ou de API's de fontes de dados de ações.
2.  **Explorar e tratar os dados**:
    * Verificar se há dados faltantes para alguma das ações no período de análise.
    * Tratar informações se necessário, removendo valores discrepantes. 
3.  **Desenvolver o modelo de otimização**.
4.  **Resolver o problema de otimização**.
5.  **Analisar os resultados**: Comparar a performance do índice com a carteira. 
6.  **Testar o modelo**: Definir um período para teste dentro da amostra e fora da amostra. [cite_start]Construir ao menos 5 carteiras fora da amostra e avaliar sua performance. 
7.  **Apresentar os resultados**: em um Jupyter Notebook.

### Referências Bibliográficas para o index-tracking:

* CORNUEJOLS, Gerard; TÜTÜNCÜ, Reha. **Optimization methods in finance**. Cambridge University Press, 2006.
* SANTANNA, L.; FILOMENA, T. P.; BORENSTEIN, D. **Index Tracking com Controle do Número de Ativos**. Revista Brasileira de Finanças, v. 12, p.89-119, 2014. 
* SANTANNA, L.; FILOMENA, T. P.; BORENSTEIN, D. GUEDES, P. **Index tracking with controlled number of assets using a hybrid heuristic combining genetic algorithm and non-linear programming**. Annals of Operations Research, v. 258, p. 449-867, 2017. 
