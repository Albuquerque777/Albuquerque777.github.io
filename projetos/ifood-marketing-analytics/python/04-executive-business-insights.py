# ============================================================
# Project: iFood Marketing Analytics
# File: 04-executive-business-insights.py
# Author: Alexander Albuquerque
# Objective:
# Generate an executive business report connecting predictive
# modeling, customer segmentation and iFood-like business pains.
# ============================================================

from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "ifood_marketing.csv"
OUTPUT_DIR = BASE_DIR / "python" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_csv_if_exists(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace(".", "_", regex=False)
    )
    return df


def get_available_columns(df: pd.DataFrame, columns: List[str]) -> List[str]:
    return [col for col in columns if col in df.columns]


def safe_divide(numerator, denominator):
    if denominator == 0 or pd.isna(denominator):
        return 0
    return numerator / denominator


def create_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    spending_columns = get_available_columns(
        df,
        ["mntwines", "mntfruits", "mntmeatproducts", "mntfishproducts", "mntsweetproducts", "mntgoldprods"],
    )
    if spending_columns and "total_spending" not in df.columns:
        df["total_spending"] = df[spending_columns].sum(axis=1)

    purchase_columns = get_available_columns(df, ["numwebpurchases", "numcatalogpurchases", "numstorepurchases"])
    if purchase_columns and "total_purchases" not in df.columns:
        df["total_purchases"] = df[purchase_columns].sum(axis=1)

    if "numdealspurchases" in df.columns and "total_purchases" in df.columns:
        df["deal_purchase_share"] = df["numdealspurchases"] / df["total_purchases"].replace(0, np.nan)
        df["deal_purchase_share"] = df["deal_purchase_share"].fillna(0)

    return df


def calculate_core_business_metrics(df: pd.DataFrame) -> dict:
    metrics = {"total_customers": len(df)}

    if "response" in df.columns:
        metrics["campaign_response_rate"] = df["response"].mean()
        metrics["campaign_responders"] = int(df["response"].sum())

    if "total_spending" in df.columns:
        metrics["total_revenue_proxy"] = df["total_spending"].sum()
        metrics["average_spending"] = df["total_spending"].mean()
        top_20_cutoff = df["total_spending"].quantile(0.80)
        top_20_spending = df.loc[df["total_spending"] >= top_20_cutoff, "total_spending"].sum()
        metrics["top_20_customer_revenue_share"] = safe_divide(top_20_spending, metrics["total_revenue_proxy"])

    if "recency" in df.columns:
        metrics["average_recency"] = df["recency"].mean()
        metrics["high_recency_customers"] = int((df["recency"] >= df["recency"].quantile(0.75)).sum())

    if "deal_purchase_share" in df.columns:
        metrics["high_discount_sensitivity_customers"] = int(
            (df["deal_purchase_share"] >= df["deal_purchase_share"].quantile(0.75)).sum()
        )

    return metrics


def build_business_pain_action_plan(metrics: dict, lift_table: pd.DataFrame, segment_profile: pd.DataFrame) -> pd.DataFrame:
    baseline = metrics.get("campaign_response_rate", np.nan)

    top_decile_lift = np.nan
    top_decile_rate = np.nan
    if not lift_table.empty and "score_decile" in lift_table.columns:
        top_decile = lift_table.sort_values("score_decile", ascending=False).head(1)
        top_decile_lift = top_decile.get("lift_vs_baseline", pd.Series([np.nan])).iloc[0]
        top_decile_rate = top_decile.get("response_rate", pd.Series([np.nan])).iloc[0]

    segment_count = len(segment_profile) if not segment_profile.empty else 0

    rows = [
        {
            "business_pain": "Campaign budget waste",
            "why_it_matters": "Sending coupons and offers to low-propensity customers reduces ROI and can increase dependence on discounts.",
            "data_insight": f"Baseline response rate: {baseline:.2%}" if not pd.isna(baseline) else "Baseline response rate unavailable.",
            "model_or_analysis": "Campaign response propensity model",
            "recommended_action": "Prioritize top propensity deciles for paid incentives and use low-cost CRM for low-propensity customers.",
            "success_kpi": "Incremental conversion, coupon cost per conversion, campaign ROI",
        },
        {
            "business_pain": "Need for personalization at scale",
            "why_it_matters": "Large delivery platforms must match users with relevant offers, restaurants, categories and timing.",
            "data_insight": f"Top decile lift: {top_decile_lift}x | Top decile response rate: {top_decile_rate:.2%}" if not pd.isna(top_decile_lift) else "Lift table unavailable.",
            "model_or_analysis": "Propensity scoring + customer segmentation",
            "recommended_action": "Use model score and segment name as campaign audience rules in CRM automation.",
            "success_kpi": "Conversion by decile, click-through rate, repeat purchase rate",
        },
        {
            "business_pain": "Customer inactivity and retention risk",
            "why_it_matters": "Inactive customers require reactivation before aggressive discount investment.",
            "data_insight": f"High-recency customers identified: {metrics.get('high_recency_customers', 'N/A')}",
            "model_or_analysis": "Recency analysis and segment action plan",
            "recommended_action": "Build win-back journeys with controlled offers, reminders and personalized categories.",
            "success_kpi": "Reactivation rate, days since last order, repeat order frequency",
        },
        {
            "business_pain": "Revenue concentration in high-value customers",
            "why_it_matters": "High-value customers should receive protection and retention journeys before they reduce frequency.",
            "data_insight": f"Top 20% revenue share: {metrics.get('top_20_customer_revenue_share', np.nan):.2%}" if not pd.isna(metrics.get('top_20_customer_revenue_share', np.nan)) else "Revenue concentration unavailable.",
            "model_or_analysis": "Customer value analysis",
            "recommended_action": "Create VIP protection strategy with premium offers, convenience bundles and early access.",
            "success_kpi": "High-value retention, average order value, purchase frequency",
        },
        {
            "business_pain": "Discount dependency and margin pressure",
            "why_it_matters": "Promotion-sensitive customers can convert, but may reduce margin if discount levels are not controlled.",
            "data_insight": f"High discount-sensitivity customers identified: {metrics.get('high_discount_sensitivity_customers', 'N/A')}",
            "model_or_analysis": "Deal purchase share analysis",
            "recommended_action": "Test lower coupon levels and bundled offers instead of broad discounts.",
            "success_kpi": "Gross margin, discount cost, conversion by discount level",
        },
        {
            "business_pain": "Need for clear executive storytelling",
            "why_it_matters": "A good data project must translate algorithms into decisions, priorities and measurable actions.",
            "data_insight": f"Generated {segment_count} actionable customer segments." if segment_count else "Segmentation output unavailable.",
            "model_or_analysis": "Executive BI + model outputs",
            "recommended_action": "Use Power BI to show segment profiles, top audiences, conversion lift and recommended CRM actions.",
            "success_kpi": "Executive adoption, campaign decision time, dashboard usage",
        },
    ]

    return pd.DataFrame(rows)


def write_markdown_report(metrics: dict, action_plan: pd.DataFrame, model_metrics: pd.DataFrame, segment_profile: pd.DataFrame) -> None:
    lines = [
        "# iFood Marketing Analytics - Executive Business Insights",
        "",
        "## Project Positioning",
        "This portfolio project connects SQL, Python, predictive modeling, customer segmentation and Power BI to solve marketing analytics problems similar to those faced by food delivery and marketplace businesses.",
        "",
        "## Core Business Objective",
        "Increase campaign efficiency, improve customer targeting, reduce discount waste, support retention and generate executive insights for marketing decisions.",
        "",
        "## Key Business Metrics",
    ]

    for key, value in metrics.items():
        if isinstance(value, float):
            if "rate" in key or "share" in key:
                value_formatted = f"{value:.2%}"
            else:
                value_formatted = f"{value:,.2f}"
        else:
            value_formatted = str(value)
        lines.append(f"- {key}: **{value_formatted}**")

    if not model_metrics.empty:
        lines.extend(["", "## Predictive Model Summary"])
        for col in model_metrics.columns:
            lines.append(f"- {col}: **{model_metrics.iloc[0][col]}**")

    if not segment_profile.empty:
        lines.extend(["", "## Customer Segmentation Summary"])
        for _, row in segment_profile.iterrows():
            segment_name = row.get("business_segment_name", "Segment")
            customers = row.get("customers", "N/A")
            action = row.get("recommended_action", "N/A")
            lines.append(f"- **{segment_name}** | Customers: {customers} | Action: {action}")

    lines.extend(["", "## Business Pain x Action Plan"])
    for _, row in action_plan.iterrows():
        lines.extend(
            [
                f"### {row['business_pain']}",
                f"- Why it matters: {row['why_it_matters']}",
                f"- Data insight: {row['data_insight']}",
                f"- Model/analysis: {row['model_or_analysis']}",
                f"- Recommended action: {row['recommended_action']}",
                f"- Success KPI: {row['success_kpi']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Limitations and Next Steps",
            "- This project uses a public/portfolio marketing dataset and should not be interpreted as official iFood data.",
            "- The predictive model estimates response propensity, not causal uplift.",
            "- The next professional step would be A/B testing, uplift modeling, recommendation ranking and integration with CRM automation.",
            "",
            "## Recommended Power BI Pages",
            "1. Executive Overview",
            "2. Campaign Response Prediction",
            "3. Customer Segmentation",
            "4. Revenue and Spending Behavior",
            "5. CRM Action Plan",
        ]
    )

    (OUTPUT_DIR / "ifood_executive_business_insights.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    raw_df = load_csv_if_exists(DATA_PATH)
    if raw_df.empty:
        raise FileNotFoundError(f"Base dataset not found: {DATA_PATH}")

    raw_df = standardize_columns(raw_df)
    raw_df = create_basic_features(raw_df)

    lift_table = load_csv_if_exists(OUTPUT_DIR / "campaign_targeting_deciles.csv")
    segment_profile = load_csv_if_exists(OUTPUT_DIR / "customer_segment_profile.csv")
    model_metrics = load_csv_if_exists(OUTPUT_DIR / "predictive_model_test_metrics.csv")

    metrics = calculate_core_business_metrics(raw_df)
    action_plan = build_business_pain_action_plan(metrics, lift_table, segment_profile)

    pd.DataFrame(list(metrics.items()), columns=["metric", "value"]).to_csv(
        OUTPUT_DIR / "executive_core_business_metrics.csv",
        index=False,
    )
    action_plan.to_csv(OUTPUT_DIR / "business_pain_action_plan.csv", index=False)
    write_markdown_report(metrics, action_plan, model_metrics, segment_profile)

    print("\n================ EXECUTIVE BUSINESS INSIGHTS COMPLETED ================")
    print(action_plan[["business_pain", "recommended_action", "success_kpi"]])
    print(f"\nOutputs saved at: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
