# iFood Marketing Analytics

Projeto completo de Marketing Analytics utilizando **SQL, Python, Machine Learning e Power BI**.

## Visão Geral

Este projeto analisa comportamento de clientes, padrões de consumo e desempenho de campanhas de marketing. Ele simula um cenário de negócio no qual uma empresa de delivery e marketplace precisa melhorar o direcionamento de campanhas, reduzir desperdício de descontos, personalizar ações de CRM e apoiar a tomada de decisão executiva.

O projeto inclui:

- Preparação de dados e KPIs em SQL
- Análise exploratória em Python
- Modelo preditivo de resposta a campanhas
- Segmentação de clientes com KMeans
- Insights executivos de negócio
- Dashboard em Power BI

> Este projeto utiliza uma base pública/educacional de marketing e não deve ser interpretado como dado oficial do iFood.

## Dashboard Power BI

[Visualizar Dashboard Power BI](https://app.powerbi.com/view?r=eyJrIjoiYjEwMTJjYmEtNTY3YS00ODRlLTgzNGYtYmUwMWEzZTM0NWYzIiwidCI6IjY1OWNlMmI4LTA3MTQtNDE5OC04YzM4LWRjOWI2MGFhYmI1NyJ9)

## Objetivos de Negócio

- Entender o comportamento e o perfil dos clientes
- Identificar clientes com maior probabilidade de resposta a campanhas
- Segmentar clientes em grupos acionáveis
- Apoiar a priorização de campanhas de CRM e marketing
- Reduzir desperdício de verba promocional e dependência de descontos
- Gerar insights executivos para tomada de decisão

## Perguntas de Negócio

- Qual é o perfil dos clientes?
- Quais clientes possuem maior gasto?
- Quais clientes têm maior probabilidade de responder a campanhas?
- Quais segmentos devem receber ofertas premium, padrão ou promocionais?
- Quais dores de negócio podem ser resolvidas com dados?
- Quais KPIs devem ser acompanhados pela liderança?

## Principais Resultados

### KPIs de Negócio

- Total de clientes: **2.205**
- Taxa de resposta da campanha: **20,77%**
- Clientes que responderam campanha: **458**
- Receita proxy analisada: **1.338.042**
- Gasto médio por cliente: **606,82**
- Participação do Top 20% dos clientes na receita: **52,28%**

### Modelo Preditivo

Foi utilizado um modelo Random Forest balanceado para estimar a probabilidade de resposta dos clientes a campanhas.

Desempenho do modelo:

- ROC-AUC: **0,8638**
- PR-AUC: **0,6606**
- Precision: **0,5620**
- Recall: **0,7391**
- F1 Score: **0,6385**

### Segmentação de Clientes

A clusterização com KMeans identificou três grupos acionáveis:

1. **Clientes de alto potencial de renda**
2. **Clientes equilibrados**
3. **Clientes sensíveis a promoção**

## Outputs Gerados

Os outputs Python estão disponíveis em:

[Python Outputs](python/outputs/)

Principais categorias de outputs:

- KPIs de negócio
- Métricas do modelo preditivo
- Predições de resposta à campanha
- Importância das variáveis
- Curva ROC
- Lift por decil
- Perfis de segmentação
- Insights executivos

## Nota de Ciência de Dados

O modelo preditivo estima propensão de resposta à campanha, não efeito causal. Para medir impacto incremental real, o próximo passo seria teste A/B, uplift modeling e simulação de ROI.

## Ferramentas

- SQL
- Python
- Pandas
- Scikit-learn
- Matplotlib
- Power BI
- Power Query
- DAX
- GitHub

## Autor

Alexander Albuquerque
