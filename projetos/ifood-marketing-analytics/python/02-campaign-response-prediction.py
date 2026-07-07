# ============================================================
# Project: iFood Marketing Analytics
# File: 02-campaign-response-prediction.py
# Author: Alexander Albuquerque
# Objective:
# Build a business-oriented predictive model to estimate which
# customers are more likely to respond to a marketing campaign.
#
# Business questions answered:
# - Which customers should receive campaign investment first?
# - Which attributes increase/decrease campaign response probability?
# - How can marketing reduce coupon waste and improve targeting?
# - Which customers should be prioritized for CRM activation?
# ============================================================

import warnings
from pathlib import Path
from typing import Dict, List, Tuple

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings("ignore")

RANDOM_STATE = 42

# ============================================================
# 1. Project paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "ifood_marketing.csv"
OUTPUT_DIR = BASE_DIR / "python" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. Utility functions
# ============================================================

def load_data(path: Path) -> pd.DataFrame:
    """Load CSV dataset. Separator is inferred automatically."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Please add the CSV file inside the data folder with the name "
            "'ifood_marketing.csv'."
        )

    return pd.read_csv(path, sep=None, engine="python")


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to snake_case."""
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
    """Return columns that exist in the dataframe."""
    return [col for col in columns if col in df.columns]


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Safely divide two series and replace infinite values with zero."""
    result = numerator / denominator.replace(0, np.nan)
    return result.replace([np.inf, -np.inf], np.nan).fillna(0)


# ============================================================
# 3. Feature engineering
# ============================================================

def create_business_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create business-oriented analytical features.

    The features are designed to solve CRM and marketing problems:
    - customer value
    - engagement level
    - discount sensitivity
    - channel preference
    - campaign history
    - inactivity risk
    """
    df = df.copy()

    # Date features
    if "dt_customer" in df.columns:
        df["dt_customer"] = pd.to_datetime(df["dt_customer"], errors="coerce", dayfirst=True)
        reference_date = df["dt_customer"].max()
        if pd.isna(reference_date):
            reference_date = pd.Timestamp.today()
        df["customer_tenure_days"] = (reference_date - df["dt_customer"]).dt.days
        reference_year = reference_date.year
    else:
        reference_year = pd.Timestamp.today().year

    # Age
    if "year_birth" in df.columns:
        df["age"] = reference_year - df["year_birth"]
        df.loc[(df["age"] < 18) | (df["age"] > 100), "age"] = np.nan

    # Product spending
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

    # Purchase channels
    purchase_columns = [
        "numwebpurchases",
        "numcatalogpurchases",
        "numstorepurchases",
    ]
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

    # Promotion sensitivity
    if "numdealspurchases" in df.columns and "total_purchases" in df.columns:
        df["deal_purchase_share"] = safe_divide(df["numdealspurchases"], df["total_purchases"])

    # Web engagement
    if "numwebvisitsmonth" in df.columns and "numwebpurchases" in df.columns:
        df["web_visit_to_purchase_ratio"] = safe_divide(
            df["numwebvisitsmonth"],
            df["numwebpurchases"] + 1,
        )

    # Household composition
    household_columns = get_available_columns(df, ["kidhome", "teenhome"])
    if household_columns:
        df["children_total"] = df[household_columns].sum(axis=1)
        df["family_size_proxy"] = 1 + df["children_total"]

    # Campaign history before latest campaign response
    previous_campaign_columns = get_available_columns(
        df,
        ["acceptedcmp1", "acceptedcmp2", "acceptedcmp3", "acceptedcmp4", "acceptedcmp5"],
    )
    if previous_campaign_columns:
        df["previous_campaign_acceptances"] = df[previous_campaign_columns].sum(axis=1)
        df["accepted_any_previous_campaign"] = (df["previous_campaign_acceptances"] > 0).astype(int)

    # Customer value groups
    if "total_spending" in df.columns:
        try:
            df["customer_value_group"] = pd.qcut(
                df["total_spending"].rank(method="first"),
                q=4,
                labels=["Low value", "Medium value", "High value", "Very high value"],
            )
        except ValueError:
            df["customer_value_group"] = "Not enough variation"

    # Inactivity risk based on recency
    if "recency" in df.columns:
        try:
            df["recency_risk_group"] = pd.qcut(
                df["recency"].rank(method="first"),
                q=4,
                labels=["Recently active", "Moderate recency", "High recency", "Very high recency risk"],
            )
        except ValueError:
            df["recency_risk_group"] = "Not enough variation"

    return df


# ============================================================
# 4. Modeling preparation
# ============================================================

def prepare_target(df: pd.DataFrame, target_col: str = "response") -> pd.DataFrame:
    """Validate and clean target variable."""
    if target_col not in df.columns:
        raise ValueError(
            f"Target column '{target_col}' was not found. "
            "This project expects a binary campaign response column named 'Response'."
        )

    df = df.copy()
    df = df[df[target_col].notna()]

    if not pd.api.types.is_numeric_dtype(df[target_col]):
        df[target_col] = df[target_col].astype(str).str.strip().str.lower().map(
            {
                "1": 1,
                "0": 0,
                "yes": 1,
                "no": 0,
                "true": 1,
                "false": 0,
                "sim": 1,
                "não": 0,
                "nao": 0,
            }
        )

    df[target_col] = df[target_col].astype(int)

    if df[target_col].nunique() < 2:
        raise ValueError("Target column must contain both classes: 0 and 1.")

    return df


def build_feature_matrix(df: pd.DataFrame, target_col: str = "response") -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """Create X/y and keep a customer reference dataframe for final outputs."""
    df = prepare_target(df, target_col=target_col)

    id_candidates = ["id", "customer_id", "client_id"]
    id_columns = get_available_columns(df, id_candidates)

    customer_reference_cols = id_columns + get_available_columns(
        df,
        [
            "age",
            "income",
            "recency",
            "total_spending",
            "total_purchases",
            "customer_value_group",
            "recency_risk_group",
        ],
    )
    customer_reference = df[customer_reference_cols].copy() if customer_reference_cols else pd.DataFrame(index=df.index)

    drop_columns = [
        target_col,
        "dt_customer",          # raw date is represented by customer_tenure_days
        "z_costcontact",        # usually constant in the public dataset
        "z_revenue",            # usually constant in the public dataset
    ] + id_columns

    X = df.drop(columns=[col for col in drop_columns if col in df.columns])
    y = df[target_col]

    # Remove columns with only one unique value, as they do not add predictive value.
    constant_columns = [col for col in X.columns if X[col].nunique(dropna=True) <= 1]
    X = X.drop(columns=constant_columns)

    return X, y, customer_reference


def make_one_hot_encoder() -> OneHotEncoder:
    """Create OneHotEncoder compatible with different scikit-learn versions."""
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """Build preprocessing pipeline for numeric and categorical features."""
    numeric_features = X.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=["number", "bool"]).columns.tolist()

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", make_one_hot_encoder()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
    )


def build_models(preprocessor: ColumnTransformer) -> Dict[str, Pipeline]:
    """Create candidate predictive models."""
    models = {
        "logistic_regression_balanced": LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            solver="liblinear",
            random_state=RANDOM_STATE,
        ),
        "random_forest_balanced": RandomForestClassifier(
            n_estimators=500,
            max_depth=None,
            min_samples_leaf=4,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "gradient_boosting": GradientBoostingClassifier(
            random_state=RANDOM_STATE,
        ),
    }

    return {
        model_name: Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )
        for model_name, model in models.items()
    }


# ============================================================
# 5. Evaluation
# ============================================================

def get_scores(model: Pipeline, X: pd.DataFrame) -> np.ndarray:
    """Return positive class probability."""
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]

    scores = model.decision_function(X)
    return (scores - scores.min()) / (scores.max() - scores.min())


def evaluate_predictions(y_true: pd.Series, y_score: np.ndarray, threshold: float = 0.50) -> Dict[str, float]:
    """Calculate model performance metrics."""
    y_pred = (y_score >= threshold).astype(int)

    metrics = {
        "threshold": round(float(threshold), 4),
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "f1_score": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "roc_auc": round(roc_auc_score(y_true, y_score), 4),
        "average_precision_pr_auc": round(average_precision_score(y_true, y_score), 4),
        "positive_rate_actual": round(float(y_true.mean()), 4),
        "positive_rate_predicted": round(float(y_pred.mean()), 4),
    }

    return metrics


def find_best_threshold(y_true: pd.Series, y_score: np.ndarray) -> float:
    """
    Find threshold that maximizes F1 score on validation data.

    Business meaning:
    - Higher recall captures more campaign responders.
    - Higher precision reduces wasted campaign spend.
    - F1 balances both.
    """
    precision, recall, thresholds = precision_recall_curve(y_true, y_score)

    if len(thresholds) == 0:
        return 0.50

    f1_scores = 2 * (precision[:-1] * recall[:-1]) / (precision[:-1] + recall[:-1] + 1e-9)
    best_index = int(np.nanargmax(f1_scores))

    return float(thresholds[best_index])


def create_lift_table(y_true: pd.Series, y_score: np.ndarray, n_bins: int = 10) -> pd.DataFrame:
    """Create decile lift table for business targeting."""
    lift_df = pd.DataFrame(
        {
            "actual_response": y_true.values,
            "response_probability": y_score,
        }
    )

    lift_df["score_decile"] = pd.qcut(
        lift_df["response_probability"].rank(method="first"),
        q=n_bins,
        labels=False,
    ) + 1

    decile_table = (
        lift_df.groupby("score_decile")
        .agg(
            customers=("actual_response", "size"),
            responders=("actual_response", "sum"),
            response_rate=("actual_response", "mean"),
            average_probability=("response_probability", "mean"),
        )
        .reset_index()
        .sort_values("score_decile", ascending=False)
    )

    baseline_response_rate = lift_df["actual_response"].mean()
    decile_table["lift_vs_baseline"] = decile_table["response_rate"] / baseline_response_rate
    decile_table["response_rate"] = decile_table["response_rate"].round(4)
    decile_table["average_probability"] = decile_table["average_probability"].round(4)
    decile_table["lift_vs_baseline"] = decile_table["lift_vs_baseline"].round(2)

    return decile_table


# ============================================================
# 6. Business outputs
# ============================================================

def classify_campaign_action(probability: float, recency_risk: str = "") -> str:
    """Translate probability into a business recommendation."""
    if probability >= 0.80:
        return "VIP priority: send high-value personalized offer"
    if probability >= 0.60:
        return "High priority: send targeted campaign"
    if probability >= 0.40:
        return "Medium priority: test offer with controlled discount"
    if "high recency" in str(recency_risk).lower():
        return "Reactivation: use low-cost push/content before discount"
    return "Low priority: avoid expensive discount, nurture organically"


def create_prediction_output(
    model: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    customer_reference: pd.DataFrame,
    threshold: float,
) -> pd.DataFrame:
    """Create customer-level campaign prediction output."""
    scores = get_scores(model, X)
    prediction_df = customer_reference.copy()
    prediction_df["actual_response"] = y.values
    prediction_df["response_probability"] = scores.round(6)
    prediction_df["predicted_response"] = (scores >= threshold).astype(int)

    prediction_df["propensity_decile"] = pd.qcut(
        prediction_df["response_probability"].rank(method="first"),
        q=10,
        labels=False,
    ) + 1

    if "recency_risk_group" in prediction_df.columns:
        prediction_df["recommended_action"] = prediction_df.apply(
            lambda row: classify_campaign_action(row["response_probability"], row["recency_risk_group"]),
            axis=1,
        )
    else:
        prediction_df["recommended_action"] = prediction_df["response_probability"].apply(classify_campaign_action)

    prediction_df = prediction_df.sort_values("response_probability", ascending=False)

    return prediction_df


def get_feature_names(model: Pipeline) -> List[str]:
    """Return transformed feature names from the preprocessing pipeline."""
    preprocessor = model.named_steps["preprocessor"]

    try:
        return preprocessor.get_feature_names_out().tolist()
    except Exception:
        feature_names = []
        for name, transformer, columns in preprocessor.transformers_:
            if name == "remainder" or transformer == "drop":
                continue
            if name == "num":
                feature_names.extend(columns)
            elif name == "cat":
                try:
                    onehot = transformer.named_steps["onehot"]
                    encoded_names = onehot.get_feature_names_out(columns).tolist()
                    feature_names.extend(encoded_names)
                except Exception:
                    feature_names.extend(columns)
        return feature_names


def extract_feature_importance(model: Pipeline) -> pd.DataFrame:
    """Extract feature importance from the selected model."""
    estimator = model.named_steps["model"]
    feature_names = get_feature_names(model)

    if hasattr(estimator, "feature_importances_"):
        importance_values = estimator.feature_importances_
    elif hasattr(estimator, "coef_"):
        importance_values = np.abs(estimator.coef_[0])
    else:
        return pd.DataFrame(columns=["feature", "importance"])

    min_len = min(len(feature_names), len(importance_values))
    importance_df = pd.DataFrame(
        {
            "feature": feature_names[:min_len],
            "importance": importance_values[:min_len],
        }
    )

    importance_df["importance"] = importance_df["importance"].astype(float)
    importance_df = importance_df.sort_values("importance", ascending=False)

    return importance_df


def create_business_action_plan(prediction_df: pd.DataFrame) -> pd.DataFrame:
    """Create actionable CRM plan from prediction results."""
    total_customers = len(prediction_df)
    high_priority = prediction_df[prediction_df["propensity_decile"] >= 9]
    low_priority = prediction_df[prediction_df["propensity_decile"] <= 3]

    action_plan = [
        {
            "business_pain": "Low campaign conversion and wasted discount budget",
            "data_insight": f"Top 20% propensity group contains {len(high_priority)} customers with the highest predicted response probability.",
            "recommended_action": "Prioritize this group for personalized campaigns, vouchers and CRM communication.",
            "kpi_to_monitor": "Campaign response rate, conversion rate, incremental revenue, coupon cost per conversion",
            "business_area": "CRM / Growth / Marketing Analytics",
        },
        {
            "business_pain": "Sending promotions to customers unlikely to convert",
            "data_insight": f"Bottom 30% propensity group contains {len(low_priority)} customers with lower predicted response probability.",
            "recommended_action": "Avoid expensive discounts for this group; use low-cost content, app notifications or organic recommendations first.",
            "kpi_to_monitor": "Discount waste, unsubscribe rate, push open rate, campaign ROI",
            "business_area": "CRM / Growth",
        },
        {
            "business_pain": "Lack of personalized decisioning",
            "data_insight": "Model ranks customers by response probability and creates a recommended action for each customer.",
            "recommended_action": "Use propensity score as a prioritization layer for marketing automation and campaign audiences.",
            "kpi_to_monitor": "Lift by decile, A/B test conversion, app conversion rate",
            "business_area": "Data / BI / Marketing Automation",
        },
        {
            "business_pain": "Retention and reactivation risk",
            "data_insight": "Recency and engagement features can identify customers who may need reactivation before discount investment.",
            "recommended_action": "Create a reactivation journey for inactive users using push notifications, reminders and controlled offers.",
            "kpi_to_monitor": "Reactivation rate, time since last purchase, repeat order rate",
            "business_area": "CRM / Lifecycle Marketing",
        },
    ]

    return pd.DataFrame(action_plan)


# ============================================================
# 7. Charts
# ============================================================

def save_roc_curve(y_true: pd.Series, y_score: np.ndarray) -> None:
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auc = roc_auc_score(y_true, y_score)

    plt.figure(figsize=(8, 5))
    plt.plot(fpr, tpr, label=f"ROC AUC = {auc:.3f}")
    plt.plot([0, 1], [0, 1], linestyle="--", label="Random baseline")
    plt.title("Campaign Response Prediction - ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "campaign_response_roc_curve.png")
    plt.close()


def save_probability_distribution(y_score: np.ndarray) -> None:
    plt.figure(figsize=(8, 5))
    pd.Series(y_score).hist(bins=30)
    plt.title("Predicted Campaign Response Probability Distribution")
    plt.xlabel("Predicted probability")
    plt.ylabel("Number of customers")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "campaign_response_probability_distribution.png")
    plt.close()


def save_lift_chart(lift_table: pd.DataFrame) -> None:
    plot_df = lift_table.sort_values("score_decile")
    plt.figure(figsize=(8, 5))
    plt.bar(plot_df["score_decile"].astype(str), plot_df["lift_vs_baseline"])
    plt.title("Campaign Response Lift by Propensity Decile")
    plt.xlabel("Propensity decile: 1 = lowest, 10 = highest")
    plt.ylabel("Lift vs baseline")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "campaign_response_lift_by_decile.png")
    plt.close()


def save_feature_importance_chart(feature_importance: pd.DataFrame, top_n: int = 20) -> None:
    if feature_importance.empty:
        return

    plot_df = feature_importance.head(top_n).sort_values("importance")
    plt.figure(figsize=(9, 7))
    plt.barh(plot_df["feature"], plot_df["importance"])
    plt.title("Top Predictive Features - Campaign Response")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "campaign_response_feature_importance.png")
    plt.close()


# ============================================================
# 8. Reports
# ============================================================

def create_markdown_report(
    best_model_name: str,
    validation_metrics: pd.DataFrame,
    test_metrics: Dict[str, float],
    lift_table: pd.DataFrame,
    feature_importance: pd.DataFrame,
    action_plan: pd.DataFrame,
) -> None:
    """Create a business-readable markdown report."""
    top_decile = lift_table.sort_values("score_decile", ascending=False).head(1)
    top_decile_lift = float(top_decile["lift_vs_baseline"].iloc[0]) if not top_decile.empty else np.nan
    top_decile_response = float(top_decile["response_rate"].iloc[0]) if not top_decile.empty else np.nan

    top_features = feature_importance.head(10)[["feature", "importance"]].copy()

    report_lines = [
        "# Campaign Response Prediction - Executive Report",
        "",
        "## Objective",
        "Predict which customers are more likely to respond to a marketing campaign and convert the model output into CRM actions.",
        "",
        "## Business Problem",
        "Food delivery and marketplace companies need to personalize communication, reduce unnecessary discount spend, reactivate customers and improve campaign conversion. This model creates a prioritization layer for campaign audiences.",
        "",
        "## Best Model",
        f"Selected model: **{best_model_name}**",
        "",
        "## Test Performance",
        f"- ROC-AUC: **{test_metrics.get('roc_auc')}**",
        f"- PR-AUC / Average Precision: **{test_metrics.get('average_precision_pr_auc')}**",
        f"- Precision: **{test_metrics.get('precision')}**",
        f"- Recall: **{test_metrics.get('recall')}**",
        f"- F1 Score: **{test_metrics.get('f1_score')}**",
        f"- Optimized Threshold: **{test_metrics.get('threshold')}**",
        "",
        "## Targeting Lift",
        f"The highest propensity decile reached a response rate of **{top_decile_response:.2%}**, representing approximately **{top_decile_lift:.2f}x** the baseline response rate.",
        "",
        "## Top Predictive Features",
    ]

    if not top_features.empty:
        for _, row in top_features.iterrows():
            report_lines.append(f"- {row['feature']}: {row['importance']:.4f}")
    else:
        report_lines.append("Feature importance was not available for the selected model.")

    report_lines.extend(
        [
            "",
            "## Business Recommendations",
        ]
    )

    for _, row in action_plan.iterrows():
        report_lines.extend(
            [
                f"### {row['business_pain']}",
                f"- Insight: {row['data_insight']}",
                f"- Recommended action: {row['recommended_action']}",
                f"- KPI to monitor: {row['kpi_to_monitor']}",
                "",
            ]
        )

    report_lines.extend(
        [
            "## Data Science Notes",
            "This model is a campaign propensity model, not a causal uplift model. To measure true incremental impact, the next step would be an A/B test or uplift modeling with treatment and control groups.",
            "",
            "## Generated Files",
            "- model_comparison_validation.csv",
            "- predictive_model_test_metrics.csv",
            "- predictive_model_classification_report.txt",
            "- predictive_model_confusion_matrix.csv",
            "- campaign_response_predictions.csv",
            "- top_100_customers_campaign_opportunity.csv",
            "- campaign_targeting_deciles.csv",
            "- campaign_response_business_action_plan.csv",
            "- campaign_response_prediction_model.joblib",
        ]
    )

    (OUTPUT_DIR / "campaign_response_prediction_executive_report.md").write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )


# ============================================================
# 9. Main execution
# ============================================================

def main() -> None:
    print("\nLoading data...")
    df = load_data(DATA_PATH)
    df = standardize_columns(df)
    df = create_business_features(df)

    print("Preparing model dataset...")
    X, y, customer_reference = build_feature_matrix(df, target_col="response")

    X_train_val, X_test, y_train_val, y_test, ref_train_val, ref_test = train_test_split(
        X,
        y,
        customer_reference,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val,
        y_train_val,
        test_size=0.25,
        random_state=RANDOM_STATE,
        stratify=y_train_val,
    )

    preprocessor = build_preprocessor(X_train)
    models = build_models(preprocessor)

    validation_results = []
    trained_models = {}

    print("Training candidate models...")
    for model_name, model in models.items():
        model.fit(X_train, y_train)
        val_scores = get_scores(model, X_val)
        val_metrics = evaluate_predictions(y_val, val_scores, threshold=0.50)
        val_metrics["model"] = model_name
        validation_results.append(val_metrics)
        trained_models[model_name] = model

    validation_metrics_df = pd.DataFrame(validation_results).sort_values(
        ["average_precision_pr_auc", "roc_auc", "f1_score"],
        ascending=False,
    )

    best_model_name = validation_metrics_df.iloc[0]["model"]
    print(f"Best model selected: {best_model_name}")

    # Refit best model with train + validation data
    best_model = build_models(build_preprocessor(X_train_val))[best_model_name]
    best_model.fit(X_train_val, y_train_val)

    # Threshold optimized using the validation set from the already trained validation model
    validation_best_model = trained_models[best_model_name]
    validation_scores = get_scores(validation_best_model, X_val)
    best_threshold = find_best_threshold(y_val, validation_scores)

    test_scores = get_scores(best_model, X_test)
    test_metrics = evaluate_predictions(y_test, test_scores, threshold=best_threshold)

    y_test_pred = (test_scores >= best_threshold).astype(int)
    class_report = classification_report(y_test, y_test_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_test_pred)

    full_predictions = create_prediction_output(
        best_model,
        X,
        y,
        customer_reference,
        threshold=best_threshold,
    )

    lift_table = create_lift_table(y, full_predictions["response_probability"].values)
    feature_importance = extract_feature_importance(best_model)
    action_plan = create_business_action_plan(full_predictions)

    # Save data outputs
    validation_metrics_df.to_csv(OUTPUT_DIR / "model_comparison_validation.csv", index=False)
    pd.DataFrame([test_metrics]).to_csv(OUTPUT_DIR / "predictive_model_test_metrics.csv", index=False)
    pd.DataFrame(cm, index=["actual_0", "actual_1"], columns=["predicted_0", "predicted_1"]).to_csv(
        OUTPUT_DIR / "predictive_model_confusion_matrix.csv"
    )
    (OUTPUT_DIR / "predictive_model_classification_report.txt").write_text(class_report, encoding="utf-8")

    full_predictions.to_csv(OUTPUT_DIR / "campaign_response_predictions.csv", index=False)
    full_predictions.head(100).to_csv(OUTPUT_DIR / "top_100_customers_campaign_opportunity.csv", index=False)
    lift_table.to_csv(OUTPUT_DIR / "campaign_targeting_deciles.csv", index=False)
    feature_importance.to_csv(OUTPUT_DIR / "campaign_response_feature_importance.csv", index=False)
    action_plan.to_csv(OUTPUT_DIR / "campaign_response_business_action_plan.csv", index=False)
    joblib.dump(best_model, OUTPUT_DIR / "campaign_response_prediction_model.joblib")

    # Save charts
    save_roc_curve(y_test, test_scores)
    save_probability_distribution(full_predictions["response_probability"].values)
    save_lift_chart(lift_table)
    save_feature_importance_chart(feature_importance)

    # Save executive report
    create_markdown_report(
        best_model_name=best_model_name,
        validation_metrics=validation_metrics_df,
        test_metrics=test_metrics,
        lift_table=lift_table,
        feature_importance=feature_importance,
        action_plan=action_plan,
    )

    print("\n================ PREDICTIVE MODEL COMPLETED ================")
    print(f"Best model: {best_model_name}")
    print(pd.DataFrame([test_metrics]).T)
    print(f"\nOutputs saved at: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
