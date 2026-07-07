# Campaign Response Prediction - Executive Report

## Objective
Predict which customers are more likely to respond to a marketing campaign and convert the model output into CRM actions.

## Business Problem
Food delivery and marketplace companies need to personalize communication, reduce unnecessary discount spend, reactivate customers and improve campaign conversion. This model creates a prioritization layer for campaign audiences.

## Best Model
Selected model: **random_forest_balanced**

## Test Performance
- ROC-AUC: **0.8638**
- PR-AUC / Average Precision: **0.6606**
- Precision: **0.562**
- Recall: **0.7391**
- F1 Score: **0.6385**
- Optimized Threshold: **0.478**

## Targeting Lift
The highest propensity decile reached a response rate of **19.46%**, representing approximately **0.94x** the baseline response rate.

## Top Predictive Features
- num__mntwines: 0.0787
- num__catalog_purchase_share: 0.0585
- num__mnttotal: 0.0533
- num__total_spending: 0.0511
- num__mntregularprods: 0.0507
- num__income: 0.0456
- num__store_purchase_share: 0.0439
- num__mntwines_share: 0.0421
- num__mntmeatproducts_share: 0.0413
- num__avg_ticket_proxy: 0.0378

## Business Recommendations
### Low campaign conversion and wasted discount budget
- Insight: Top 20% propensity group contains 441 customers with the highest predicted response probability.
- Recommended action: Prioritize this group for personalized campaigns, vouchers and CRM communication.
- KPI to monitor: Campaign response rate, conversion rate, incremental revenue, coupon cost per conversion

### Sending promotions to customers unlikely to convert
- Insight: Bottom 30% propensity group contains 662 customers with lower predicted response probability.
- Recommended action: Avoid expensive discounts for this group; use low-cost content, app notifications or organic recommendations first.
- KPI to monitor: Discount waste, unsubscribe rate, push open rate, campaign ROI

### Lack of personalized decisioning
- Insight: Model ranks customers by response probability and creates a recommended action for each customer.
- Recommended action: Use propensity score as a prioritization layer for marketing automation and campaign audiences.
- KPI to monitor: Lift by decile, A/B test conversion, app conversion rate

### Retention and reactivation risk
- Insight: Recency and engagement features can identify customers who may need reactivation before discount investment.
- Recommended action: Create a reactivation journey for inactive users using push notifications, reminders and controlled offers.
- KPI to monitor: Reactivation rate, time since last purchase, repeat order rate

## Data Science Notes
This model is a campaign propensity model, not a causal uplift model. To measure true incremental impact, the next step would be an A/B test or uplift modeling with treatment and control groups.

## Generated Files
- model_comparison_validation.csv
- predictive_model_test_metrics.csv
- predictive_model_classification_report.txt
- predictive_model_confusion_matrix.csv
- campaign_response_predictions.csv
- top_100_customers_campaign_opportunity.csv
- campaign_targeting_deciles.csv
- campaign_response_business_action_plan.csv
- campaign_response_prediction_model.joblib