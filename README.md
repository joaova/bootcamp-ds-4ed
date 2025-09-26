# bootcamp-ds-4ed
Repositório do Grupo 1 do Bootcamp de Introdução à Data Science - Edição 2025/2

# Bootcamp de Introdução a Data Science: PROJETO FINOR

## Briefing Técnico

### Problemática Inicial

[cite_start]Os modelos de *index tracking* buscam reproduzir o comportamento de índices de ações com um número de ações inferior ao do índice original, simplificando a composição do portfólio e, consequentemente, o custo de manutenção do portfólio. [cite: 3]

### Objetivo

[cite_start]O objetivo desse projeto é desenvolver um modelo de *index tracking* para os índices S&P100 e IBOV. [cite: 4]

### Motivação

[cite_start]Os índices de mercado (por exemplo, S&P500) são compostos por ações individuais e representam termômetros dos mercados de ações. [cite: 6] [cite_start]Fundos de investimento passivo visam replicar o desempenho de um índice de mercado ou de um segmento específico do mercado. [cite: 7]

### Dados

[cite_start]Os participantes devem buscar os dados históricos dos últimos 7 anos dos índices S&P 100 e IBOVESPA para serem utilizados como inputs. [cite: 8] [cite_start]Os dados podem ser encontrados no Yahoo Finance e outros locais de interesse do grupo. [cite: 9]

### Modelo Matemático

[cite_start]O modelo de otimização a ser utilizado é o seguinte: [cite: 10]

**Minimizar:**
$$ \frac{1}{T}\sum_{t=1}^{T}(\sum_{i \in I}w_{i}r_{t,i}-R_{t})^{2} $$

**Sujeito a:**
$$ \sum_{i \in I}w_{i}=1 $$
$$ w_{i} \ge 0 \quad \forall i \in I $$
$$ w_{i} \le z_{i} \quad \forall i \in I $$
$$ \sum_{i \in I}z_{i} \le K $$
$$ z_{i} \in \{0,1\} \quad \forall i \in I $$

**Onde:**
* [cite_start]**I**: conjunto de ativos disponíveis [cite: 19]
* [cite_start]**T**: número de períodos [cite: 20]
* [cite_start]**$w_{i}$**: Peso do ativo *i* no portfólio de tracking [cite: 21]
* [cite_start]**$z_{i}$**: Variável binária (0,1) para o ativo *i* [cite: 18, 22]
* [cite_start]**$R_{t}$**: Rendimento do índice no período *t* [cite: 23]
* [cite_start]**$r_{t,i}$**: Rendimento do ativo *i* no período *t* [cite: 24, 25]
* [cite_start]**K**: Número máximo de ativos permitidos [cite: 26]

### Index tracking (IT)

* [cite_start]IT consiste em uma estratégia de replicar um índice de mercado utilizando um número menor de ações. [cite: 29]
* [cite_start]IT apresenta menores custos e, por ter menos ativos, fornece uma carteira de ações mais simples de ser gerida. [cite: 30]
* [cite_start]IT no formato de problema de otimização pode ser incrementado com restrições de negócio. [cite: 31]

### Etapas

[cite_start]A implementação do modelo de otimização deve ser realizada em Python, podendo ser utilizadas API's de Python de solvers como Gurobi ou de solvers open-source. [cite: 34]

1.  [cite_start]**Importar os dados**: a partir de arquivos ou de API's de fontes de dados de ações. [cite: 36]
2.  **Explorar e tratar os dados**:
    * [cite_start]Verificar se há dados faltantes para alguma das ações no período de análise. [cite: 38, 39]
    * [cite_start]Tratar informações se necessário, removendo valores discrepantes. [cite: 40, 41]
3.  [cite_start]**Desenvolver o modelo de otimização**. [cite: 42]
4.  [cite_start]**Resolver o problema de otimização**. [cite: 43]
5.  [cite_start]**Analisar os resultados**: Comparar a performance do índice com a carteira. [cite: 44]
6.  **Testar o modelo**: Definir um período para teste dentro da amostra e fora da amostra. [cite_start]Construir ao menos 5 carteiras fora da amostra e avaliar sua performance. [cite: 45]
7.  [cite_start]**Apresentar os resultados**: em um Jupyter Notebook. [cite: 46]

### Referências Bibliográficas para o index-tracking:

* CORNUEJOLS, Gerard; TÜTÜNCÜ, Reha. **Optimization methods in finance**. [cite_start]Cambridge University Press, 2006. [cite: 48]
* SANTANNA, L.; FILOMENA, T. P.; BORENSTEIN, D. **Index Tracking com Controle do Número de Ativos**. Revista Brasileira de Finanças, v. 12, p. [cite_start]89-119, 2014. [cite: 49, 50]
* SANTANNA, L.; FILOMENA, T. P.; BORENSTEIN, D. GUEDES, P. **Index tracking with controlled number of assets using a hybrid heuristic combining genetic algorithm and non-linear programming**. Annals of Operations Research, v. 258, p. [cite_start]449-867, 2017. [cite: 51, 52, 53, 54, 55]
