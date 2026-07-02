# iFood Marketing Analytics

## Sobre o projeto

Este projeto tem como objetivo analisar dados de clientes e campanhas de marketing, simulando um cenário de negócio em que a empresa precisa entender melhor o perfil dos consumidores, identificar padrões de compra e melhorar a efetividade das campanhas comerciais.

A solução foi desenvolvida utilizando SQL para modelagem e tratamento dos dados, Power BI para construção de indicadores e visualização executiva, e Python para futuras análises exploratórias e segmentação de clientes.

---

## Problema de negócio

A empresa precisa responder perguntas como:

- Qual é o perfil dos clientes com maior consumo?
- Quais clientes possuem maior potencial de resposta a campanhas?
- Como os clientes se comportam por faixa de renda e faixa etária?
- Quais canais de compra são mais utilizados?
- Qual é a taxa de resposta das campanhas?
- Existem clientes de alta renda com baixo consumo que podem ser melhor trabalhados?

---

## Objetivos da análise

- Tratar e organizar os dados de clientes.
- Criar indicadores executivos de negócio.
- Segmentar clientes por renda, idade, consumo e resposta a campanhas.
- Gerar consultas analíticas para apoiar decisões de marketing.
- Preparar uma base estruturada para dashboards em Power BI.

---

## Ferramentas utilizadas

- SQL
- Power BI
- Power Query
- DAX
- Python
- GitHub

---

## Estrutura do projeto

```text
ifood-marketing-analytics/
│
├── sql/
│   ├── 01-criacao-tabelas.sql
│   ├── 02tratamentodados.sql
│   ├── 03-kpis-negocio.sql
│   └── 04-segmentacao-clientes.sql
│
├── powerbi/
│
└── python/
## Etapas em SQL

Nesta etapa foram criados scripts SQL para estruturar, tratar e analisar os dados do projeto.

### 1. Criação da tabela

Arquivo: `01-criacao-tabelas.sql`

Este arquivo cria a tabela principal do projeto, com informações sobre clientes, renda, compras, campanhas e reclamações.

### 2. Tratamento dos dados

Arquivo: `02tratamentodados.sql`

Este arquivo cria uma visão tratada da base, calculando novos campos como idade, total de dependentes, gasto total e total de compras.

### 3. Indicadores de negócio

Arquivo: `03-kpis-negocio.sql`

Este arquivo cria indicadores executivos, como total de clientes, renda média, gasto médio, total de compras e taxa de resposta das campanhas.

### 4. Segmentação de clientes

Arquivo: `04-segmentacao-clientes.sql`

Este arquivo segmenta os clientes por faixa etária, faixa de renda, perfil de consumo, perfil de compra e resposta à campanha.

---

## Principais indicadores analisados

- Total de clientes
- Renda média
- Idade média
- Receita total analisada
- Gasto médio por cliente
- Média de compras por cliente
- Taxa de resposta de campanha
- Taxa de reclamação
- Consumo por faixa de renda
- Consumo por faixa etária

---



## Autor

Alexander Albuquerque


