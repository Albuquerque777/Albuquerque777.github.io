# Python Analytics Layer

This folder contains the Python analytics layer of the iFood Marketing Analytics project.

## Scripts

### 01 - Exploratory Analysis

File: `01-exploratory-analysis.py`

Performs:

- Data loading
- Column standardization
- Feature engineering
- Business KPI calculation
- Exploratory charts
- Treated dataset export

### 02 - Campaign Response Prediction

File: `02-campaign-response-prediction.py`

Builds a predictive model to estimate customer campaign response probability.

Main outputs:

- Model comparison metrics
- Test performance metrics
- Campaign response predictions
- Feature importance
- ROC curve
- Lift by decile
- Top customers with higher response probability

### 03 - Customer Segmentation Advanced

File: `03-customer-segmentation-advanced.py`

Applies KMeans clustering to segment customers into actionable business groups.

Main outputs:

- Customer segment classification
- Segment profiles
- Segment action plan
- PCA visualization
- Silhouette score comparison

### 04 - Executive Business Insights

File: `04-executive-business-insights.py`

Generates executive business insights by connecting KPIs, model results, segmentation and business pains.

Main outputs:

- Business pain action plan
- Executive business insights report
- Recommended actions and success KPIs

## How to Run

From this folder, run:

```bash
python -m pip install -r requirements.txt
python 01-exploratory-analysis.py
python 02-campaign-response-prediction.py
python 03-customer-segmentation-advanced.py
python 04-executive-business-insights.py
```

## Outputs

Generated outputs are available in:

[`outputs/`](outputs/)

## Data Science Note

The predictive model estimates campaign response propensity, not causal uplift. For production use, the next step would be A/B testing, uplift modeling and ROI simulation.
