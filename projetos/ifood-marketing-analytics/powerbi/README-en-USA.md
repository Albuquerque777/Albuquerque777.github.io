# Power BI - iFood Marketing Analytics

## About This Folder

This folder contains the Power BI stage of the iFood Marketing Analytics project.

The objective is to transform the treated and analyzed data into an executive dashboard focused on customer behavior, consumption patterns and marketing campaign performance.

---

## Dashboard Objective

The Power BI dashboard aims to provide a clear and executive view of the main business indicators related to customers and marketing campaigns.

The dashboard will help answer questions such as:

- What is the customer profile?
- Which customer segments generate the highest spending?
- What is the campaign response rate?
- Which purchase channels are most used?
- How does consumption vary by age group and income range?
- Which customers represent potential marketing opportunities?

---

## Planned Dashboard Pages

### 1. Executive Overview

Main business KPIs and general project summary.

Expected indicators:

- Total customers
- Total revenue analyzed
- Average income
- Average customer age
- Average spending per customer
- Average purchases per customer
- Campaign response rate
- Complaint rate

---

### 2. Customer Profile

Customer demographic and behavioral analysis.

Expected visuals:

- Customers by age group
- Customers by income range
- Customers by education level
- Customers by marital status
- Dependents per customer

---

### 3. Consumption Analysis

Analysis of customer spending behavior.

Expected visuals:

- Total spending by product category
- Average spending by age group
- Average spending by income range
- High-value customer groups
- Purchase behavior by channel

---

### 4. Campaign Performance

Marketing campaign performance analysis.

Expected visuals:

- Campaign response rate
- Responses by income range
- Responses by age group
- Responses by consumption segment
- Comparison between customers who responded and did not respond

---

### 5. Customer Segmentation

Customer grouping based on income, age, spending and campaign response.

Expected segments:

- High-value customers
- Medium-value customers
- Low-value customers
- High-income customers with low consumption
- Customers with high campaign response potential

---

## Tools Used

- Power BI
- Power Query
- DAX
- SQL
- Python
- Data Modeling
- Business Intelligence

---

## Expected Files

```text
powerbi/
│
├── README.md
├── dashboard-ifood.pbix
├── dashboard-ifood.pdf
│
└── images/
    ├── executive-overview.png
    ├── customer-profile.png
    ├── consumption-analysis.png
    ├── campaign-performance.png
    └── customer-segmentation.png
```

---

## Planned DAX Measures

Examples of expected DAX measures:

```DAX
Total Customers = COUNTROWS(Customers)

Total Revenue = SUM(Customers[Total Spending])

Average Income = AVERAGE(Customers[Income])

Average Spending = AVERAGE(Customers[Total Spending])

Campaign Response Rate =
DIVIDE(
    SUM(Customers[Response]),
    COUNTROWS(Customers)
)
```

---

## Expected Business Value

The Power BI dashboard will support business decision-making by presenting customer behavior and marketing performance in a clear, visual and executive format.

The dashboard can help the business:

- Improve marketing campaign targeting
- Identify high-value customer segments
- Understand consumption behavior
- Monitor campaign performance
- Support data-driven decision-making

---

## Status

Power BI dashboard development is planned as the next stage of the project after the SQL and Python steps.

---

## Author

Alexander Albuquerque

Senior Process Analyst | Data & BI | SQL | Power BI | Python | Data Engineering | IT Project Management | Automation
