# iFood Marketing Analytics

End-to-end Marketing Analytics project using **SQL, Python, Machine Learning and Power BI**.

## Overview

This project analyzes customer behavior, consumption patterns and marketing campaign performance. It simulates a business scenario where a food delivery and marketplace company needs to improve campaign targeting, reduce discount waste, personalize CRM actions and support executive decision-making.

The project includes:

- SQL data preparation and business KPIs
- Python exploratory analysis
- Campaign response prediction model
- Customer segmentation with KMeans
- Executive business insights
- Power BI dashboard

> This project uses a public/educational marketing dataset and should not be interpreted as official iFood data.

## Power BI Dashboard

[View Power BI Dashboard](https://app.powerbi.com/view?r=eyJrIjoiYjEwMTJjYmEtNTY3YS00ODRlLTgzNGYtYmUwMWEzZTM0NWYzIiwidCI6IjY1OWNlMmI4LTA3MTQtNDE5OC04YzM4LWRjOWI2MGFhYmI1NyJ9)

## Business Objectives

- Understand customer behavior and spending patterns
- Identify customers with higher campaign response probability
- Segment customers into actionable business groups
- Support CRM and marketing campaign prioritization
- Reduce campaign budget waste and discount dependency
- Generate executive insights for decision-making

## Key Questions

- What is the customer profile?
- Which customers have higher spending?
- Which customers are more likely to respond to campaigns?
- Which customer segments should receive premium, standard or promotional offers?
- Which business pains can be solved with data and analytics?
- What KPIs should be monitored by executives?

## Main Results

### Business KPIs

- Total customers: **2,205**
- Campaign response rate: **20.77%**
- Campaign responders: **458**
- Total revenue proxy: **1,338,042**
- Average spending per customer: **606.82**
- Top 20% customer revenue share: **52.28%**

### Predictive Model

A balanced Random Forest model was used to estimate campaign response probability.

Model performance:

- ROC-AUC: **0.8638**
- PR-AUC: **0.6606**
- Precision: **0.5620**
- Recall: **0.7391**
- F1 Score: **0.6385**

### Customer Segmentation

KMeans clustering identified three actionable customer groups:

1. **High-income potential customers**
2. **Balanced customers**
3. **Promotion-sensitive customers**

## Generated Outputs

Python outputs are available in:

[Python Outputs](python/outputs/)

Main output categories:

- Business KPIs
- Predictive model metrics
- Campaign response predictions
- Feature importance
- ROC curve
- Lift by decile
- Customer segmentation profiles
- Executive business insights

## Data Science Note

The predictive model estimates campaign response propensity, not causal uplift. To measure true incremental impact, the next step would be A/B testing, uplift modeling and ROI simulation.

## Tools

- SQL
- Python
- Pandas
- Scikit-learn
- Matplotlib
- Power BI
- Power Query
- DAX
- GitHub

## Author

Alexander Albuquerque
