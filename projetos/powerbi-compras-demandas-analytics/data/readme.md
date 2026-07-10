# Power BI - Compras, Demandas e Comparativo 

## Sobre o projeto

Este projeto apresenta um conjunto de dashboards desenvolvidos em Power BI para análise executiva de **Compras**, **Demandas** e do **comparativo entre as duas bases**.

O objetivo é demonstrar como dados operacionais podem ser transformados em indicadores executivos para acompanhamento de carteira, análise de status, processos em andamento, resultados encerrados, inconsistências cadastrais e cobertura entre bases.

Os arquivos foram organizados para fins de portfólio profissional. Antes de publicar, revise se todos os dados, nomes, IDs, clientes e informações sensíveis estão anonimizados.

---

## Dashboards incluídos

### 1. Relatório de Compras

Painel voltado para análise dos processos formais de compra, contratação, cotação ou aquisição.

Principais análises:

- Total de processos de compras
- Valor total da carteira
- Processos em andamento
- Processos ganhos
- Processos sem contratação
- Taxa de conclusão
- Aging dos processos em aberto
- Encerrados por ganho e sem contratação
- Distribuição por gestor, torre, tipo de contratação e tipo de registro

Principais abas:

- Visão Geral
- Em Andamento
- Encerrados

---

### 2. Relatório de Demandas

Painel voltado para análise da carteira de demandas, oportunidades ou necessidades registradas para acompanhamento comercial e operacional.

Principais análises:

- Total de demandas
- Valor total da carteira
- Demandas ganhas
- Demandas perdidas
- Demandas em andamento
- Win Rate
- Distribuição por etapa, probabilidade, gestor e produto/solução
- Evolução mensal das oportunidades

Principais abas:

- Visão Geral
- Em Andamento
- Concluídos
- Detalhamento
- Inconsistências

---

### 3. Comparativo Compras x Demandas

Painel voltado para análise de cobertura cadastral entre processos de Compras e a base de Demandas.

O objetivo é identificar:

- Processos de Compras localizados em Demandas
- Processos de Compras não localizados em Demandas
- Registros existentes somente em Demandas
- Pendências de ID ou Projeto
- Duplicidades cadastrais
- Impacto financeiro das inconsistências
- Índice de cobertura por gestor

---

## Diferença entre Compras e Demandas

**Demandas** representam oportunidades, projetos ou necessidades registradas para acompanhamento da carteira.

**Compras** representam processos formais de contratação, cotação ou aquisição relacionados a essas necessidades.

De forma simples:

```text
Demandas = oportunidades, necessidades ou projetos acompanhados.
Compras = processos formais de contratação, cotação ou aquisição.
```

Nem toda demanda necessariamente vira um processo de compras, e nem todo processo de compras será comparável diretamente com a base total de demandas, pois as bases podem ter períodos, regras e finalidades diferentes.

---

## Principais indicadores

### Compras

| Indicador | Descrição |
|---|---|
| Total Processos | Quantidade total de processos de compras analisados |
| Valor Total | Soma financeira dos processos |
| Em Andamento | Processos ainda abertos ou em tratativa |
| Ganho | Processos concluídos com sucesso |
| Sem Contratação | Processos cancelados, perdidos, recusados ou declinados |
| Taxa de Conclusão | Percentual de processos ganhos sobre o total da carteira |
| Taxa de Sucesso | Percentual de ganhos considerando apenas processos encerrados |
| Aging | Tempo em que um processo permanece aberto |

### Demandas

| Indicador | Descrição |
|---|---|
| Total Demandas | Quantidade total de demandas ou oportunidades |
| Valor Total | Soma financeira das demandas |
| Qtd Ganho | Demandas encerradas com sucesso |
| Valor Ganho | Valor financeiro das demandas ganhas |
| Qtd Perdido | Demandas encerradas sem sucesso |
| Valor Perdido | Valor financeiro das demandas perdidas |
| Em Andamento | Demandas ainda abertas ou em negociação |
| Win Rate | Percentual de demandas ganhas entre as demandas encerradas |

### Comparativo Compras x Demandas

| Indicador | Descrição |
|---|---|
| Localizado | Processo de Compras encontrado na base de Demandas |
| Não Localizado | Processo de Compras não encontrado em Demandas ou com falha cadastral |
| Somente Demandas | Registro existente apenas na base de Demandas |
| Índice de Cobertura | Percentual de processos de Compras localizados em Demandas |
| Duplicidade | Registro com chave, ID ou projeto duplicado |

---

## Glossário e siglas

| Sigla / Termo | Significado |
|---|---|
| PT | Etapa técnica do processo |
| PC | Proposta comercial |
| PT e PC | Processo que envolve análise técnica e proposta comercial |
| RFP | Request for Proposal, solicitação de proposta |
| RFQ | Request for Quotation, solicitação de cotação |
| RFI | Request for Information, solicitação de informação |
| Aging | Tempo em aberto desde a data de entrada |
| Ticket Médio | Valor médio por processo |
| Win Rate | Taxa de ganho |
| Opportunity | Nova oportunidade |
| Renewal | Renovação |
| Addendum | Aditivo contratual |
| Quente | Alta probabilidade de conversão |
| Morno | Probabilidade intermediária de conversão |
| Frio | Baixa probabilidade de conversão |

---

## Regras de negócio

### Compras

Os processos de compras foram agrupados em três classificações principais:

```text
Ganho
Em Andamento
Sem Contratação
```

A classificação **Sem Contratação** consolida processos com status como:

```text
Cancelado
Perdido
Declinado
Recusado
```

### Encerrados

A aba Encerrados considera:

```text
Ganho + Sem Contratação
```

Essa visão permite analisar o resultado final dos processos já concluídos, separando o que virou ganho do que foi encerrado sem contratação.

### Em Andamento

A aba Em Andamento considera apenas processos ainda abertos ou em tratativa.

Essa visão é usada para acompanhamento operacional, priorização por aging, valor em aberto e identificação de responsáveis.

---

## Principais análises

### Visão Geral

A visão geral apresenta o resumo executivo da carteira, permitindo avaliar rapidamente:

- Volume total de processos
- Valor financeiro total
- Quantidade em andamento
- Quantidade ganha
- Quantidade sem contratação
- Taxa de conclusão
- Distribuição por status, gestor, torre, contratação e registro

### Em Andamento

A análise de processos em andamento permite identificar:

- Processos abertos
- Valor ainda em tratativa
- Aging médio
- Maior aging
- Principais processos críticos
- Responsáveis com maior concentração de valor
- Torres com maior volume em aberto

### Encerrados

A análise de encerrados permite avaliar:

- Total de processos finalizados
- Valor encerrado
- Ganhos
- Processos sem contratação
- Taxa de sucesso
- Tempo de conclusão
- Principais processos encerrados por valor

---

## Ferramentas utilizadas

- Power BI
- Power Query
- DAX
- Modelagem de dados
- Tratamento e padronização de dados
- Visualização executiva
- Análise de indicadores
- Storytelling com dados

---

## Competências demonstradas

- Business Intelligence
- Data Analytics
- Power BI
- Power Query
- DAX
- Modelagem dimensional
- Indicadores executivos
- Tratamento de dados
- Análise de processos de compras
- Análise de demandas e oportunidades
- Gestão de inconsistências cadastrais
- Criação de dashboards para tomada de decisão

---

## Observação sobre os dados

Os dados utilizados neste projeto devem estar anonimizados e adaptados para fins de portfólio.

Informações sensíveis, nomes reais, identificadores internos e dados comerciais confidenciais devem ser removidos ou substituídos por valores genéricos antes da publicação.

---

## Prints do projeto

### Relatório de Compras - Visão Geral

![Compras Visão Geral](images/compras-visao-geral.png)

### Relatório de Compras - Em Andamento

![Compras Em Andamento](images/compras-em-andamento.png)

### Relatório de Compras - Encerrados

![Compras Encerrados](images/compras-encerrados.png)

### Relatório de Demandas - Visão Geral

![Demandas Visão Geral](images/demandas-visao-geral.png)

### Comparativo Compras x Demandas

![Comparativo Compras x Demandas](images/comparativo-compras-demandas.png)

---

## Arquivos do projeto

```text
dashboards/
├── comparativo-compras-demandas.pbix
├── relatorio-compras.pbix
└── relatorio-demandas.pbix

images/
├── compras-visao-geral.png
├── compras-em-andamento.png
├── compras-encerrados.png
├── demandas-visao-geral.png
└── comparativo-compras-demandas.png
```

---

## Autor

Alexander Albuquerque

Profissional de Dados, BI, Automação e Eficiência Operacional, com foco em transformar dados complexos em indicadores executivos, apoiar a tomada de decisão e melhorar a visibilidade operacional por meio de dashboards e análises estruturadas.
