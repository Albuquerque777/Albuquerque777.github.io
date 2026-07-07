# iFood Marketing Analytics - Predictive Analytics Upgrade

This upgrade adds a more advanced business-oriented analytics layer to the iFood Marketing Analytics portfolio project.

> Important: this is a portfolio project using a public/educational marketing dataset. It should not be interpreted as official iFood data.

## Business Context

Food delivery and marketplace businesses need to improve personalization, customer retention, campaign conversion and marketing ROI. This project transforms a marketing dataset into a decision-support solution using Python, machine learning, customer segmentation and Power BI.

## Business Pains Addressed

1. **Campaign budget waste**  
   Avoid sending coupons to customers with low probability of conversion.

2. **Low campaign response rate**  
   Rank customers by response probability and prioritize high-propensity audiences.

3. **Need for personalization at scale**  
   Segment customers into actionable groups for CRM, lifecycle marketing and recommendations.

4. **Retention and reactivation risk**  
   Identify customers with high recency/inactivity risk and create reactivation journeys.

5. **Discount dependency and margin pressure**  
   Identify promotion-sensitive customers and test controlled discount strategies.

6. **Executive decision-making**  
   Generate clear metrics, actions and insights that can be presented in Power BI.

## Python Scripts

### 01 - Exploratory Analysis
Existing script that performs data loading, feature engineering, KPI calculation and basic charts.

### 02 - Campaign Response Prediction
File: `02-campaign-response-prediction.py`

Builds a predictive model to estimate customer probability of responding to a campaign.

Models tested:
- Logistic Regression with balanced class weights
- Random Forest with balanced class weights
- Gradient Boosting

Generated outputs:
- `model_comparison_validation.csv`
- `predictive_model_test_metrics.csv`
- `predictive_model_classification_report.txt`
- `predictive_model_confusion_matrix.csv`
- `campaign_response_predictions.csv`
- `top_100_customers_campaign_opportunity.csv`
- `campaign_targeting_deciles.csv`
- `campaign_response_feature_importance.csv`
- `campaign_response_business_action_plan.csv`
- `campaign_response_prediction_executive_report.md`
- `campaign_response_prediction_model.joblib`

### 03 - Customer Segmentation Advanced
File: `03-customer-segmentation-advanced.py`

Segments customers into business-oriented groups using KMeans and silhouette score.

Generated outputs:
- `customer_segments.csv`
- `customer_segment_profile.csv`
- `customer_segment_action_plan.csv`
- `segmentation_silhouette_scores.csv`
- `customer_segmentation_executive_report.md`
- `customer_segmentation_model.joblib`

### 04 - Executive Business Insights
File: `04-executive-business-insights.py`

Consolidates model, segmentation and business metrics into an executive report.

Generated outputs:
- `executive_core_business_metrics.csv`
- `business_pain_action_plan.csv`
- `ifood_executive_business_insights.md`

## How to Run

From the project root:

```bash
cd projetos/ifood-marketing-analytics/python
pip install -r requirements.txt
python 01-exploratory-analysis.py
python 02-campaign-response-prediction.py
python 03-customer-segmentation-advanced.py
python 04-executive-business-insights.py
```

## Recommended Power BI Pages

1. **Executive Overview**
   - Total customers
   - Average income
   - Total spending
   - Campaign response rate
   - Model ROC-AUC / PR-AUC
   - Top decile lift

2. **Campaign Prediction**
   - Response probability distribution
   - Customers by propensity decile
   - Response rate by decile
   - Top 100 campaign opportunities
   - Recommended action by customer

3. **Customer Segmentation**
   - Segment size
   - Average spending by segment
   - Average recency by segment
   - Segment action plan

4. **Marketing Efficiency**
   - Discount-sensitive customers
   - High-value customers
   - Low-propensity customers
   - Campaign ROI proxy

5. **Executive Action Plan**
   - Business pain
   - Data insight
   - Recommended action
   - KPI to monitor
   - Business area

## Portfolio Positioning

This project demonstrates:

- SQL analysis
- Python data analysis
- Feature engineering
- Predictive modeling
- Customer segmentation
- Business insight generation
- Power BI storytelling
- Marketing analytics
- CRM decision support

## Suggested LinkedIn Description

Predictive Marketing Analytics project using SQL, Python, Scikit-learn and Power BI to analyze customer behavior, predict campaign response, segment customers and generate CRM action plans. The project addresses business problems such as campaign conversion, discount waste, retention risk, personalization and executive decision-making.
