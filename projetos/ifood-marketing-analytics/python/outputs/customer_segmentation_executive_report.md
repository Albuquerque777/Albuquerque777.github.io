# Customer Segmentation - Executive Report

## Objective
Segment customers into actionable groups to support personalization, CRM journeys, retention and marketing campaign strategy.

## Methodology
KMeans clustering was tested for different values of K. The selected number of clusters was **3**, based on silhouette score.

## Silhouette Scores
|   k |   silhouette_score |
|----:|-------------------:|
|   3 |             0.1886 |
|   5 |             0.1515 |
|   4 |             0.1514 |
|   6 |             0.1386 |
|   7 |             0.1187 |
|   8 |             0.1148 |

## Segment Profiles and Recommended Actions
### Segment 0 - High-income potential customers
- Customers: 752
- Customer share: 34.10%
- Main business pain: Customers with purchasing power but not necessarily maximum conversion
- Recommended action: Test premium categories, convenience bundles and quality-focused communication.
- Campaign strategy: Premium offers, quality communication, high-ticket categories. Prioritize because historical response is above baseline.

### Segment 1 - Balanced customers
- Customers: 845
- Customer share: 38.32%
- Main business pain: General audience requiring standard personalization
- Recommended action: Use standard segmented campaigns and monitor migration to other groups.
- Campaign strategy: Baseline CRM, seasonal campaigns, category-based recommendations.

### Segment 2 - Promotion-sensitive customers
- Customers: 608
- Customer share: 27.57%
- Main business pain: Margin pressure caused by customers highly dependent on discounts
- Recommended action: Use controlled discounts and test minimum discount needed to convert.
- Campaign strategy: A/B test coupon levels, bundles, limited-time offers.

## Business Value
This segmentation can be used to personalize offers, prioritize CRM journeys, reduce discount waste, protect high-value customers and improve lifecycle marketing decisions.

## Generated Files
- customer_segments.csv
- customer_segment_profile.csv
- customer_segment_action_plan.csv
- segmentation_silhouette_scores.csv
- customer_segmentation_model.joblib