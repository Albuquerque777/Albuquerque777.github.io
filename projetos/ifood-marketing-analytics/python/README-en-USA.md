# Python - iFood Marketing Analytics

## About This Folder

This folder contains the Python analysis for the iFood Marketing Analytics project.

The objective is to explore customer behavior, consumption patterns and marketing campaign performance using Python. This analysis supports the creation of business indicators, customer segmentation and future predictive models.

---

## Objective

The Python stage aims to:

- Load and inspect the dataset.
- Identify missing values and data quality issues.
- Create analytical variables.
- Calculate customer age.
- Calculate total customer spending.
- Calculate total purchases.
- Analyze income and consumption behavior.
- Analyze marketing campaign response.
- Generate business KPIs.
- Export treated datasets and analytical outputs.
- Prepare the data for Power BI dashboards and future machine learning models.

---

## Tools and Libraries

- Python
- pandas
- numpy
- matplotlib
- scikit-learn

---

## Folder Structure

```text
python/
│
├── README.md
├── requirements.txt
├── 01_exploratory_analysis.py
│
└── outputs/
    ├── ifood_marketing_treated.csv
    ├── business_kpis.csv
    ├── income_distribution.png
    ├── total_spending_distribution.png
    ├── average_spending_by_age_group.png
    └── response_rate_by_income_group.png
```

---

## Main Script

### `01_exploratory_analysis.py`

This script performs the exploratory data analysis of the iFood marketing dataset.

Main steps:

1. Load the dataset.
2. Standardize column names.
3. Create analytical features.
4. Calculate business KPIs.
5. Export treated data.
6. Generate charts.
7. Save outputs for documentation and future Power BI use.

---

## Expected Dataset

The script expects the dataset to be located in:

```text
../data/ifood_marketing.csv
```

Expected file name:

```text
ifood_marketing.csv
```

The dataset must be anonymized and should not contain sensitive personal information.

---

## Generated Outputs

The script creates an `outputs` folder containing treated data, business KPIs and charts.

Expected outputs:

```text
outputs/
├── ifood_marketing_treated.csv
├── business_kpis.csv
├── income_distribution.png
├── total_spending_distribution.png
├── average_spending_by_age_group.png
└── response_rate_by_income_group.png
```

---

## Business Questions Supported

This Python analysis helps answer questions such as:

- What is the average customer income?
- What is the average customer age?
- Which customer groups spend the most?
- How is spending distributed across customers?
- What is the campaign response rate?
- Which income groups respond better to campaigns?
- Which age groups have higher average spending?
- How can the dataset be prepared for Power BI dashboards?

---

## Future Improvements

Future Python developments may include:

- Customer clustering.
- RFM analysis.
- Campaign response prediction.
- Propensity model for marketing campaigns.
- Feature importance analysis.
- Export of scored customer lists for business use.

---

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the exploratory analysis:

```bash
python 01_exploratory_analysis.py
```

---

## Author

Alexander Albuquerque

Senior Process Analyst | Data & BI | SQL | Power BI | Python | Data Engineering | IT Project Management | Automation
