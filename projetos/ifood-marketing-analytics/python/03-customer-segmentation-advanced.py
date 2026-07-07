# ============================================================
# Project: iFood Marketing Analytics
# File: 03-customer-segmentation-advanced.py
# Author: Alexander Albuquerque
# Objective:
# Segment customers into business-oriented groups to support
# personalization, CRM journeys, retention and campaign strategy.
# ============================================================

import warnings
from pathlib import Path
from typing import Dict, List

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
RANDOM_STATE = 42

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "ifood_marketing.csv"
OUTPUT_DIR = BASE_DIR / "python" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Please add the CSV file inside the data folder with the name 'ifood_marketing.csv'."
        )
    return pd.read_csv(path, sep=None, engine="python")


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


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    result = numerator / denominator.replace(0, np.nan)
    return result.replace([np.inf, -np.inf], np.nan).fillna(0)


def create_segmentation_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create features focused on customer segmentation."""
    df = df.copy()

    if "dt_customer" in df.columns:
        df["dt_customer"] = pd.to_datetime(df["dt_customer"], errors="coerce", dayfirst=True)
        reference_date = df["dt_customer"].max()
        if pd.isna(reference_date):
            reference_date = pd.Timestamp.today()
        df["customer_tenure_days"] = (reference_date - df["dt_customer"]).dt.days
        reference_year = reference_date.year
    else:
        reference_year = pd.Timestamp.today().year

    if "year_birth" in df.columns:
        df["age"] = reference_year - df["year_birth"]
        df.loc[(df["age"] < 18) | (df["age"] > 100), "age"] = np.nan

    spending_columns = [
        "mntwines",
        "mntfruits",
        "mntmeatproducts",
        "mntfishproducts",
        "mntsweetproducts",
        "mntgoldprods",
    ]
    available_spending_columns = get_available_columns(df, spending_columns)
    if available_spending_columns:
        df["total_spending"] = df[available_spending_columns].sum(axis=1)
        for col in available_spending_columns:
            df[f"{col}_share"] = safe_divide(df[col], df["total_spending"])

    purchase_columns = ["numwebpurchases", "numcatalogpurchases", "numstorepurchases"]
    available_purchase_columns = get_available_columns(df, purchase_columns)
    if available_purchase_columns:
        df["total_purchases"] = df[available_purchase_columns].sum(axis=1)
        df["avg_ticket_proxy"] = safe_divide(df.get("total_spending", 0), df["total_purchases"])
        if "numwebpurchases" in df.columns:
            df["web_purchase_share"] = safe_divide(df["numwebpurchases"], df["total_purchases"])
        if "numcatalogpurchases" in df.columns:
            df["catalog_purchase_share"] = safe_divide(df["numcatalogpurchases"], df["total_purchases"])
        if "numstorepurchases" in df.columns:
            df["store_purchase_share"] = safe_divide(df["numstorepurchases"], df["total_purchases"])

    if "numdealspurchases" in df.columns and "total_purchases" in df.columns:
        df["deal_purchase_share"] = safe_divide(df["numdealspurchases"], df["total_purchases"])

    if "numwebvisitsmonth" in df.columns and "numwebpurchases" in df.columns:
        df["web_visit_to_purchase_ratio"] = safe_divide(df["numwebvisitsmonth"], df["numwebpurchases"] + 1)

    household_columns = get_available_columns(df, ["kidhome", "teenhome"])
    if household_columns:
        df["children_total"] = df[household_columns].sum(axis=1)
        df["family_size_proxy"] = 1 + df["children_total"]

    previous_campaign_columns = get_available_columns(
        df,
        ["acceptedcmp1", "acceptedcmp2", "acceptedcmp3", "acceptedcmp4", "acceptedcmp5"],
    )
    if previous_campaign_columns:
        df["previous_campaign_acceptances"] = df[previous_campaign_columns].sum(axis=1)
        df["accepted_any_previous_campaign"] = (df["previous_campaign_acceptances"] > 0).astype(int)

    return df


def select_segmentation_features(df: pd.DataFrame) -> List[str]:
    """Select business-relevant numeric features for clustering."""
    candidate_features = [
        "income",
        "age",
        "recency",
        "customer_tenure_days",
        "total_spending",
        "total_purchases",
        "avg_ticket_proxy",
        "web_purchase_share",
        "catalog_purchase_share",
        "store_purchase_share",
        "deal_purchase_share",
        "web_visit_to_purchase_ratio",
        "children_total",
        "family_size_proxy",
        "previous_campaign_acceptances",
        "accepted_any_previous_campaign",
        "mntwines_share",
        "mntfruits_share",
        "mntmeatproducts_share",
        "mntfishproducts_share",
        "mntsweetproducts_share",
        "mntgoldprods_share",
    ]

    features = get_available_columns(df, candidate_features)
    features = [feature for feature in features if pd.api.types.is_numeric_dtype(df[feature])]

    if len(features) < 3:
        raise ValueError(
            "Not enough numeric features for segmentation. "
            "Please check if the dataset has income, spending, purchase and recency columns."
        )

    return features


def build_clustering_matrix(df: pd.DataFrame, features: List[str]) -> np.ndarray:
    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    return pipeline.fit_transform(df[features]), pipeline


def choose_best_k(X_scaled: np.ndarray, min_k: int = 3, max_k: int = 8) -> pd.DataFrame:
    """Choose the number of clusters using silhouette score."""
    max_possible_k = min(max_k, len(X_scaled) - 1)
    scores = []

    for k in range(min_k, max_possible_k + 1):
        model = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=20)
        labels = model.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        scores.append({"k": k, "silhouette_score": round(float(score), 4)})

    scores_df = pd.DataFrame(scores)
    if scores_df.empty:
        raise ValueError("Not enough rows to calculate clustering silhouette score.")

    return scores_df.sort_values("silhouette_score", ascending=False)


def assign_business_segment_names(profile: pd.DataFrame, global_profile: Dict[str, float]) -> pd.DataFrame:
    """Assign interpretable names and actions to clusters."""
    profile = profile.copy()

    segment_names = []
    main_pains = []
    recommended_actions = []
    campaign_strategies = []

    for _, row in profile.iterrows():
        spending = row.get("total_spending_mean", np.nan)
        recency = row.get("recency_mean", np.nan)
        income = row.get("income_mean", np.nan)
        deal_share = row.get("deal_purchase_share_mean", np.nan)
        web_share = row.get("web_purchase_share_mean", np.nan)
        previous_acceptance = row.get("previous_campaign_acceptances_mean", 0)
        response_rate = row.get("response_mean", np.nan)

        high_spending = spending >= global_profile.get("total_spending_q75", np.inf)
        low_spending = spending <= global_profile.get("total_spending_q25", -np.inf)
        high_recency = recency >= global_profile.get("recency_q75", np.inf)
        low_recency = recency <= global_profile.get("recency_q25", -np.inf)
        high_income = income >= global_profile.get("income_q75", np.inf)
        high_deal = deal_share >= global_profile.get("deal_purchase_share_q75", np.inf)
        high_digital = web_share >= global_profile.get("web_purchase_share_q75", np.inf)
        strong_campaign_history = previous_acceptance > global_profile.get("previous_campaign_acceptances_mean", 0)

        if high_spending and low_recency:
            name = "High-value engaged customers"
            pain = "Protecting high-value customers from churn and maintaining frequency"
            action = "Create VIP journey, premium recommendations and early access offers."
            strategy = "Personalized offer, loyalty communication, cross-sell bundles."
        elif high_spending and high_recency:
            name = "High-value at-risk customers"
            pain = "Important customers are becoming inactive"
            action = "Run reactivation journey with personalized incentive and urgency-based communication."
            strategy = "Win-back campaign, personalized coupon, reactivation push."
        elif high_deal:
            name = "Promotion-sensitive customers"
            pain = "Margin pressure caused by customers highly dependent on discounts"
            action = "Use controlled discounts and test minimum discount needed to convert."
            strategy = "A/B test coupon levels, bundles, limited-time offers."
        elif high_digital:
            name = "Digital-first customers"
            pain = "Need to increase app/web conversion and personalize digital channels"
            action = "Prioritize app recommendations, push notifications and personalized collections."
            strategy = "App-first campaign, recommendation carousel, category personalization."
        elif low_spending and high_recency:
            name = "Low-engagement inactive customers"
            pain = "Low engagement and low recent purchase behavior"
            action = "Use low-cost nurturing before offering expensive incentives."
            strategy = "Educational content, small test offer, reminder journey."
        elif strong_campaign_history:
            name = "Campaign-responsive customers"
            pain = "Need to scale response among customers with positive campaign history"
            action = "Prioritize for campaign launches and similar audience expansion."
            strategy = "New campaign tests, personalized categories, lookalike audience."
        elif high_income:
            name = "High-income potential customers"
            pain = "Customers with purchasing power but not necessarily maximum conversion"
            action = "Test premium categories, convenience bundles and quality-focused communication."
            strategy = "Premium offers, quality communication, high-ticket categories."
        else:
            name = "Balanced customers"
            pain = "General audience requiring standard personalization"
            action = "Use standard segmented campaigns and monitor migration to other groups."
            strategy = "Baseline CRM, seasonal campaigns, category-based recommendations."

        if not pd.isna(response_rate) and response_rate >= global_profile.get("response_mean", 1):
            strategy += " Prioritize because historical response is above baseline."

        segment_names.append(name)
        main_pains.append(pain)
        recommended_actions.append(action)
        campaign_strategies.append(strategy)

    profile["business_segment_name"] = segment_names
    profile["main_business_pain"] = main_pains
    profile["recommended_action"] = recommended_actions
    profile["campaign_strategy"] = campaign_strategies

    return profile


def create_segment_profile(df: pd.DataFrame, features: List[str]) -> pd.DataFrame:
    aggregation = {feature: ["mean", "median"] for feature in features}
    if "response" in df.columns:
        aggregation["response"] = ["mean", "sum"]

    profile = df.groupby("customer_segment").agg(aggregation)
    profile.columns = ["_".join(col).strip() for col in profile.columns.values]
    profile["customers"] = df.groupby("customer_segment").size()
    profile["customer_share"] = profile["customers"] / len(df)
    profile = profile.reset_index()

    global_profile = {}
    for col in ["total_spending", "recency", "income", "deal_purchase_share", "web_purchase_share"]:
        if col in df.columns:
            global_profile[f"{col}_q25"] = df[col].quantile(0.25)
            global_profile[f"{col}_q75"] = df[col].quantile(0.75)
            global_profile[f"{col}_mean"] = df[col].mean()
    if "previous_campaign_acceptances" in df.columns:
        global_profile["previous_campaign_acceptances_mean"] = df["previous_campaign_acceptances"].mean()
    if "response" in df.columns:
        global_profile["response_mean"] = df["response"].mean()

    profile = assign_business_segment_names(profile, global_profile)
    profile["customer_share"] = profile["customer_share"].round(4)

    return profile


def create_segment_action_plan(profile: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "customer_segment",
        "business_segment_name",
        "customers",
        "customer_share",
        "main_business_pain",
        "recommended_action",
        "campaign_strategy",
    ]
    return profile[[col for col in cols if col in profile.columns]].copy()


def save_charts(df: pd.DataFrame, profile: pd.DataFrame, X_scaled: np.ndarray) -> None:
    # Segment size
    segment_size = df["customer_segment_name"].value_counts().sort_values()
    plt.figure(figsize=(10, 6))
    plt.barh(segment_size.index.astype(str), segment_size.values)
    plt.title("Customer Segment Size")
    plt.xlabel("Number of customers")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "customer_segment_size.png")
    plt.close()

    # Spending by segment
    if "total_spending" in df.columns:
        spending_by_segment = df.groupby("customer_segment_name")["total_spending"].mean().sort_values()
        plt.figure(figsize=(10, 6))
        plt.barh(spending_by_segment.index.astype(str), spending_by_segment.values)
        plt.title("Average Spending by Customer Segment")
        plt.xlabel("Average spending")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "average_spending_by_customer_segment.png")
        plt.close()

    # Recency by segment
    if "recency" in df.columns:
        recency_by_segment = df.groupby("customer_segment_name")["recency"].mean().sort_values()
        plt.figure(figsize=(10, 6))
        plt.barh(recency_by_segment.index.astype(str), recency_by_segment.values)
        plt.title("Average Recency by Customer Segment")
        plt.xlabel("Average recency")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "average_recency_by_customer_segment.png")
        plt.close()

    # PCA visualization
    if X_scaled.shape[0] >= 3 and X_scaled.shape[1] >= 2:
        pca = PCA(n_components=2, random_state=RANDOM_STATE)
        components = pca.fit_transform(X_scaled)
        plt.figure(figsize=(8, 6))
        plt.scatter(components[:, 0], components[:, 1], c=df["customer_segment"], alpha=0.7)
        plt.title("Customer Segments - PCA View")
        plt.xlabel("PCA component 1")
        plt.ylabel("PCA component 2")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "customer_segments_pca_view.png")
        plt.close()


def create_markdown_report(profile: pd.DataFrame, scores_df: pd.DataFrame, best_k: int) -> None:
    report = [
        "# Customer Segmentation - Executive Report",
        "",
        "## Objective",
        "Segment customers into actionable groups to support personalization, CRM journeys, retention and marketing campaign strategy.",
        "",
        "## Methodology",
        f"KMeans clustering was tested for different values of K. The selected number of clusters was **{best_k}**, based on silhouette score.",
        "",
        "## Silhouette Scores",
        scores_df.to_markdown(index=False),
        "",
        "## Segment Profiles and Recommended Actions",
    ]

    for _, row in profile.iterrows():
        report.extend(
            [
                f"### Segment {row['customer_segment']} - {row['business_segment_name']}",
                f"- Customers: {row['customers']}",
                f"- Customer share: {row['customer_share']:.2%}",
                f"- Main business pain: {row['main_business_pain']}",
                f"- Recommended action: {row['recommended_action']}",
                f"- Campaign strategy: {row['campaign_strategy']}",
                "",
            ]
        )

    report.extend(
        [
            "## Business Value",
            "This segmentation can be used to personalize offers, prioritize CRM journeys, reduce discount waste, protect high-value customers and improve lifecycle marketing decisions.",
            "",
            "## Generated Files",
            "- customer_segments.csv",
            "- customer_segment_profile.csv",
            "- customer_segment_action_plan.csv",
            "- segmentation_silhouette_scores.csv",
            "- customer_segmentation_model.joblib",
        ]
    )

    (OUTPUT_DIR / "customer_segmentation_executive_report.md").write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    print("\nLoading data...")
    df = load_data(DATA_PATH)
    df = standardize_columns(df)
    df = create_segmentation_features(df)

    features = select_segmentation_features(df)
    print(f"Selected segmentation features: {features}")

    X_scaled, preprocessing_pipeline = build_clustering_matrix(df, features)

    scores_df = choose_best_k(X_scaled)
    best_k = int(scores_df.iloc[0]["k"])
    print(f"Best K selected: {best_k}")

    kmeans = KMeans(n_clusters=best_k, random_state=RANDOM_STATE, n_init=20)
    df["customer_segment"] = kmeans.fit_predict(X_scaled)

    profile = create_segment_profile(df, features)
    action_plan = create_segment_action_plan(profile)

    segment_name_map = dict(zip(profile["customer_segment"], profile["business_segment_name"]))
    df["customer_segment_name"] = df["customer_segment"].map(segment_name_map)

    # Save outputs
    df.to_csv(OUTPUT_DIR / "customer_segments.csv", index=False)
    profile.to_csv(OUTPUT_DIR / "customer_segment_profile.csv", index=False)
    action_plan.to_csv(OUTPUT_DIR / "customer_segment_action_plan.csv", index=False)
    scores_df.to_csv(OUTPUT_DIR / "segmentation_silhouette_scores.csv", index=False)

    joblib.dump(
        {
            "preprocessing_pipeline": preprocessing_pipeline,
            "kmeans_model": kmeans,
            "features": features,
            "segment_name_map": segment_name_map,
        },
        OUTPUT_DIR / "customer_segmentation_model.joblib",
    )

    save_charts(df, profile, X_scaled)
    create_markdown_report(profile, scores_df, best_k)

    print("\n================ CUSTOMER SEGMENTATION COMPLETED ================")
    print(profile[["customer_segment", "business_segment_name", "customers", "customer_share", "recommended_action"]])
    print(f"\nOutputs saved at: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
