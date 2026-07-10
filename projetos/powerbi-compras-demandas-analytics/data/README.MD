# Data

## Sobre os Dados

Esta pasta foi criada para documentar a origem, estrutura e cuidados relacionados aos dados utilizados no projeto **Power BI - Compras, Demandas e Cobertura Cadastral**.

Por questões de segurança, privacidade e confidencialidade, as bases originais utilizadas na construção dos dashboards **não estão disponíveis neste repositório**.

O projeto foi publicado apenas com documentação, imagens e explicações das regras de negócio, utilizando dados anonimizados/adaptados para fins de portfólio.

---

## Bases Utilizadas no Projeto

O projeto foi construído a partir de três grupos principais de dados:

### 1. Base de Compras

Representa os processos formais de contratação, cotação, negociação ou aquisição.

Principais informações analisadas:

- ID do processo
- Projeto
- Status da contratação
- Valor do processo
- Data de entrada
- Data de fechamento
- Gestor responsável
- Torre ou área responsável
- Tipo de contratação
- Tipo de registro
- Etapa da contratação

---

### 2. Base de Demandas

Representa oportunidades, projetos, necessidades ou iniciativas registradas para acompanhamento da carteira.

Principais informações analisadas:

- ID da oportunidade
- Nome da demanda/oportunidade
- Status da demanda
- Valor da oportunidade
- Data de criação
- Data de fechamento
- Gestor responsável
- Etapa comercial
- Probabilidade
- Produto ou solução
- Tipo de registro

---

### 3. Base Comparativa Compras x Demandas

Representa o cruzamento entre os processos de Compras e a base de Demandas.

O objetivo dessa base é identificar:

- Processos de Compras localizados em Demandas
- Processos de Compras não localizados em Demandas
- Registros existentes somente em Demandas
- Pendências de ID ou Projeto
- Duplicidades cadastrais
- Divergências de valor
- Índice de cobertura entre as bases

---

## Observação sobre Privacidade

As bases originais não foram incluídas neste repositório porque podem conter informações sensíveis, como:

- Identificadores internos
- Valores comerciais
- Informações de clientes
- Nomes de responsáveis
- Dados operacionais
- Caminhos de arquivos ou conexões corporativas

Para fins de portfólio, os dados foram tratados, anonimizados ou representados visualmente por meio dos dashboards e imagens do projeto.

---

## Dados Disponíveis no Repositório

Este repositório contém apenas:

- Prints dos dashboards
- Documentação do projeto
- Regras de negócio
- Glossário
- Explicação dos indicadores
- Links publicados dos relatórios, quando disponíveis

Os arquivos `.pbix` e as bases originais não são disponibilizados publicamente.

---

## Estrutura Esperada dos Dados

Caso este projeto fosse reproduzido com uma base sintética, a estrutura mínima recomendada seria:

### Compras

| Campo | Descrição |
|---|---|
| ID_PROCESSO | Identificador do processo de compras |
| PROJETO | Código ou nome do projeto |
| STATUS_CONTRATACAO | Status do processo |
| STATUS_MACRO | Classificação macro: Ganho, Em Andamento ou Sem Contratação |
| VALOR | Valor financeiro do processo |
| DATA_ENTRADA | Data de entrada do processo |
| DATA_FECHAMENTO | Data de fechamento ou encerramento |
| GESTOR | Responsável pelo processo |
| TORRE | Área ou torre responsável |
| TIPO_CONTRATACAO | Novo, Renovação ou Aditivo |
| TIPO_REGISTRO | RFP, RFQ ou RFI |
| ETAPA_CONTRATACAO | PT, PC ou PT e PC |

---

### Demandas

| Campo | Descrição |
|---|---|
| ID_DEMANDA | Identificador da demanda ou oportunidade |
| NOME_DEMANDA | Nome da demanda ou oportunidade |
| STATUS_DEMANDA | Status da demanda |
| STATUS_MACRO | Encerrada ou Em Andamento |
| VALOR | Valor financeiro da demanda |
| DATA_CRIACAO | Data de criação da demanda |
| DATA_FECHAMENTO | Data de fechamento da demanda |
| GESTOR | Responsável pela demanda |
| ETAPA | Etapa comercial ou operacional |
| PROBABILIDADE | Quente, Morno ou Frio |
| PRODUTO_SOLUCAO | Produto ou solução associado |
| TIPO_REGISTRO | Opportunity, Renewal ou Addendum |

---

### Comparativo Compras x Demandas

| Campo | Descrição |
|---|---|
| ID_COMPRAS | Identificador do processo de compras |
| ID_DEMANDA | Identificador da demanda |
| PROJETO_COMPRAS | Projeto informado em Compras |
| PROJETO_DEMANDAS | Projeto informado em Demandas |
| STATUS_COMPARATIVO | Localizado, Não Localizado ou Somente Demandas |
| VALOR_COMPRAS | Valor do processo de compras |
| VALOR_DEMANDAS | Valor da demanda |
| GESTOR | Gestor responsável |
| FLAG_DUPLICIDADE | Indica se há duplicidade |
| FLAG_DIVERGENCIA_VALOR | Indica se há divergência de valor |
| FLAG_EXISTE_COMPRAS | Indica existência na base de Compras |
| FLAG_EXISTE_DEMANDAS | Indica existência na base de Demandas |

---

## Finalidade

Esta pasta serve apenas para documentar o contexto das bases utilizadas no projeto.

O foco do repositório é demonstrar competências em:

- Power BI
- Power Query
- DAX
- Modelagem de dados
- Indicadores executivos
- Tratamento e padronização de dados
- Análise de Compras
- Análise de Demandas
- Comparativo entre bases
- Storytelling com dados
