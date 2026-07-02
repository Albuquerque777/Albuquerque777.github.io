# iFood Marketing Analytics

🇧🇷 Portuguese version: [README-pt-BR.md](README-pt-BR.md)

## About the Project

This project aims to analyze customer data and marketing campaign performance, simulating a business scenario in which the company needs to better understand customer profiles, identify purchasing patterns and improve the effectiveness of marketing campaigns.

The solution was developed using SQL for data modeling and data preparation, Power BI for executive dashboarding and data visualization, and Python for exploratory analysis and customer segmentation.

---

## Business Problem

The company needs to answer questions such as:

- What is the profile of the highest-spending customers?
- Which customers have the highest potential to respond to marketing campaigns?
- How do customers behave by income range and age group?
- Which purchase channels are most used?
- What is the campaign response rate?
- Are there high-income customers with low consumption who could be better targeted?

---

## Analysis Objectives

- Clean, organize and structure customer data.
- Create executive business indicators.
- Segment customers by income, age, consumption and campaign response.
- Generate analytical queries to support marketing decisions.
- Prepare a structured dataset for Power BI dashboards.
- Support future exploratory analysis and predictive models in Python.

---

## Tools Used

- SQL
- Power BI
- Power Query
- DAX
- Python
- GitHub

---

## Project Structure

```text
ifood-marketing-analytics/
│
├── README.md
├── README-pt-BR.md
│
├── sql/
│   ├── 01-criacao-tabelas.sql
│   ├── 02tratamentodados.sql
│   ├── 03-kpis-negocio.sql
│   └── 04-segmentacao-clientes.sql
│
├── python/
│   ├── README.md
│   ├── requirements.txt
│   └── 01_exploratory_analysis.py
│
├── data/
│   └── README.md
│
└── powerbi/
```

---

## SQL Steps

At this stage, SQL scripts were created to structure, clean and analyze the project data.

### 1. Table Creation

File: `01-criacao-tabelas.sql`

This file creates the main project table, containing information about customers, income, purchases, marketing campaigns and complaints.

### 2. Data Preparation

File: `02tratamentodados.sql`

This file creates a cleaned analytical view of the dataset, calculating new fields such as age, total dependents, total spending and total purchases.

### 3. Business Indicators

File: `03-kpis-negocio.sql`

This file creates executive KPIs such as total customers, average income, average spending, total purchases and campaign response rate.

### 4. Customer Segmentation

File: `04-segmentacao-clientes.sql`

This file segments customers by age group, income range, consumption profile, purchase behavior and campaign response.

---

## Python Steps

The Python stage aims to support exploratory analysis, data validation, feature creation and future customer segmentation.

Planned analyses include:

- Data loading and inspection
- Missing value analysis
- Customer age calculation
- Total spending calculation
- Total purchases calculation
- Income and consumption analysis
- Campaign response analysis
- Customer segmentation
- Preparation for future predictive models

---

## Power BI Steps

The Power BI stage will be used to build an executive dashboard based on the treated and analyzed data.

Planned dashboard pages:

- Executive Overview
- Customer Profile
- Consumption Analysis
- Campaign Performance
- Customer Segmentation

---

## Main Indicators Analyzed

- Total customers
- Average income
- Average age
- Total revenue analyzed
- Average spending per customer
- Average purchases per customer
- Campaign response rate
- Complaint rate
- Consumption by income range
- Consumption by age group
- High-value customers
- High-income customers with low consumption

---

## Expected Business Value

This project demonstrates how data can be used to support marketing decisions by identifying customer segments, consumption patterns and campaign opportunities.

The analysis can help the business:

- Improve campaign targeting
- Identify high-value customer groups
- Understand customer purchasing behavior
- Support executive decision-making with KPIs
- Prepare data for BI dashboards and future predictive models

---

## Next Steps

- Upload the anonymized dataset.
- Run the exploratory analysis in Python.
- Generate analytical outputs and charts.
- Build the executive dashboard in Power BI.
- Add dashboard screenshots to the project.
- Create customer segmentation analysis.
- Develop a future campaign response propensity model.

---

## Author

Alexander Albuquerque

Senior Process Analyst | Data & BI | SQL | Power BI | Python | Data Engineering | IT Project Management | Automation
