# iFood Marketing Analytics - Executive Business Insights

## Project Positioning
This portfolio project connects SQL, Python, predictive modeling, customer segmentation and Power BI to solve marketing analytics problems similar to those faced by food delivery and marketplace businesses.

## Core Business Objective
Increase campaign efficiency, improve customer targeting, reduce discount waste, support retention and generate executive insights for marketing decisions.

## Key Business Metrics
- total_customers: **2205**
- campaign_response_rate: **20.77%**
- campaign_responders: **458**
- total_revenue_proxy: **1338042**
- average_spending: **606.82**
- top_20_customer_revenue_share: **52.28%**
- average_recency: **49.01**
- high_recency_customers: **563**
- high_discount_sensitivity_customers: **749**

## Predictive Model Summary
- threshold: **0.478**
- accuracy: **0.8254**
- precision: **0.562**
- recall: **0.7391**
- f1_score: **0.6385**
- roc_auc: **0.8638**
- average_precision_pr_auc: **0.6606**
- positive_rate_actual: **0.2086**
- positive_rate_predicted: **0.2744**

## Customer Segmentation Summary
- **High-income potential customers** | Customers: 752 | Action: Test premium categories, convenience bundles and quality-focused communication.
- **Balanced customers** | Customers: 845 | Action: Use standard segmented campaigns and monitor migration to other groups.
- **Promotion-sensitive customers** | Customers: 608 | Action: Use controlled discounts and test minimum discount needed to convert.

## Business Pain x Action Plan
### Campaign budget waste
- Why it matters: Sending coupons and offers to low-propensity customers reduces ROI and can increase dependence on discounts.
- Data insight: Baseline response rate: 20.77%
- Model/analysis: Campaign response propensity model
- Recommended action: Prioritize top propensity deciles for paid incentives and use low-cost CRM for low-propensity customers.
- Success KPI: Incremental conversion, coupon cost per conversion, campaign ROI

### Need for personalization at scale
- Why it matters: Large delivery platforms must match users with relevant offers, restaurants, categories and timing.
- Data insight: Top decile lift: 0.94x | Top decile response rate: 19.46%
- Model/analysis: Propensity scoring + customer segmentation
- Recommended action: Use model score and segment name as campaign audience rules in CRM automation.
- Success KPI: Conversion by decile, click-through rate, repeat purchase rate

### Customer inactivity and retention risk
- Why it matters: Inactive customers require reactivation before aggressive discount investment.
- Data insight: High-recency customers identified: 563
- Model/analysis: Recency analysis and segment action plan
- Recommended action: Build win-back journeys with controlled offers, reminders and personalized categories.
- Success KPI: Reactivation rate, days since last order, repeat order frequency

### Revenue concentration in high-value customers
- Why it matters: High-value customers should receive protection and retention journeys before they reduce frequency.
- Data insight: Top 20% revenue share: 52.28%
- Model/analysis: Customer value analysis
- Recommended action: Create VIP protection strategy with premium offers, convenience bundles and early access.
- Success KPI: High-value retention, average order value, purchase frequency

### Discount dependency and margin pressure
- Why it matters: Promotion-sensitive customers can convert, but may reduce margin if discount levels are not controlled.
- Data insight: High discount-sensitivity customers identified: 749
- Model/analysis: Deal purchase share analysis
- Recommended action: Test lower coupon levels and bundled offers instead of broad discounts.
- Success KPI: Gross margin, discount cost, conversion by discount level

### Need for clear executive storytelling
- Why it matters: A good data project must translate algorithms into decisions, priorities and measurable actions.
- Data insight: Generated 3 actionable customer segments.
- Model/analysis: Executive BI + model outputs
- Recommended action: Use Power BI to show segment profiles, top audiences, conversion lift and recommended CRM actions.
- Success KPI: Executive adoption, campaign decision time, dashboard usage

## Limitations and Next Steps
- This project uses a public/portfolio marketing dataset and should not be interpreted as official iFood data.
- The predictive model estimates response propensity, not causal uplift.
- The next professional step would be A/B testing, uplift modeling, recommendation ranking and integration with CRM automation.

## Recommended Power BI Pages
1. Executive Overview
2. Campaign Response Prediction
3. Customer Segmentation
4. Revenue and Spending Behavior
5. CRM Action Plan