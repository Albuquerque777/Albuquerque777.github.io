# iFood Marketing Analytics

End-to-end Marketing Analytics portfolio project using **SQL, Python, Machine Learning and Power BI**.

## Project Overview

This project simulates a business scenario for a food delivery and marketplace company that needs to understand customer behavior, improve campaign targeting, reduce discount waste, support retention strategies and generate executive insights for marketing decisions.

The solution combines SQL, Python, predictive modeling, customer segmentation and Power BI to transform customer and campaign data into actionable business recommendations.

> **Important note:** this project uses a public/educational marketing dataset and should not be interpreted as official iFood data.

## Live Dashboard

[View Power BI Dashboard](https://app.powerbi.com/view?r=eyJrIjoiYjEwMTJjYmEtNTY3YS00ODRlLTgzNGYtYmUwMWEzZTM0NWYzIiwidCI6IjY1OWNlMmI4LTA3MTQtNDE5OC04YzM4LWRjOWI2MGFhYmI1NyJ9)

## Main Business Questions

- Which customers are more likely to respond to marketing campaigns?
- Which customer segments should receive premium offers, standard campaigns or controlled discounts?
- How can campaign budget waste be reduced?
- Which customers should be prioritized for CRM actions?
- How concentrated is revenue among high-value customers?
- What KPIs should executives monitor?

## Project Layers

### SQL

Used for table creation, data preparation, business KPIs and customer segmentation queries.

Folder: [`sql/`](sql/)

### Python

Used for exploratory analysis, feature engineering, campaign response prediction, customer segmentation and executive insights.

Folder: [`python/`](python/)

### Machine Learning

A balanced Random Forest model was used to estimate customer campaign response probability.

Main model results:

- ROC-AUC: **0.8638**
- PR-AUC: **0.6606**
- Precision: **0.5620**
- Recall: **0.7391**
- F1 Score: **0.6385**

### Customer Segmentation

KMeans clustering identified three actionable customer groups:

- **High-income potential customers**
- **Balanced customers**
- **Promotion-sensitive customers**

### Power BI

Used to create an executive dashboard for customer behavior, campaign performance, segmentation and business insights.

Folder: [`powerbi/`](powerbi/)

## Key Business Metrics

- Total customers: **2,205**
- Campaign response rate: **20.77%**
- Campaign responders: **458**
- Total revenue proxy: **1,338,042**
- Average spending per customer: **606.82**
- Top 20% customer revenue share: **52.28%**

## Generated Outputs

The Python scripts generate analytical outputs including business KPIs, predictive model metrics, campaign response predictions, customer segmentation results, charts and executive business insights.

Main outputs are available in:

[Python Outputs](python/outputs/)

Examples of generated outputs:

- Business KPIs
- Predictive model performance metrics
- Campaign response predictions
- Customer targeting deciles
- Customer segment profiles
- Business pain action plan
- Executive business insights report
- Exploratory analysis charts

## Data Science Note

This model estimates **campaign response propensity**, not causal uplift.

Although the model achieved strong ROC-AUC, the lift-by-decile analysis indicates that campaign targeting should be validated through A/B testing before production use.

Recommended next steps:

- A/B testing
- Uplift modeling
- Probability calibration
- ROI simulation
- CRM automation integration

## Tools Used

- SQL
- Python
- Pandas
- Scikit-learn
- Matplotlib
- Power BI
- Power Query
- DAX
- GitHub

## Repository Structure

```text
ifood-marketing-analytics/
├── data/
├── powerbi/
├── python/
│   ├── outputs/
│   ├── 01-exploratory-analysis.py
│   ├── 02-campaign-response-prediction.py
│   ├── 03-customer-segmentation-advanced.py
│   ├── 04-executive-business-insights.py
│   └── requirements.txt
├── sql/
├── README.md
├── README-en-USA.md
└── README-pt-BR.md
```

## Author

Alexander Albuquerque  
Data & BI | SQL | Power BI | Python | Machine Learning | IT Project Management | Automation
