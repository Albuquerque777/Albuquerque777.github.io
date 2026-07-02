# ============================================================
# Project: iFood Marketing Analytics
# File: 01-exploratory-analysis.py
# Author: Alexander Albuquerque
# Objective:
# Perform an exploratory data analysis of customer behavior,
# consumption patterns and marketing campaign response.
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# 1. Project paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "ifood_marketing.csv"
OUTPUT_DIR = BASE_DIR / "python" / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. Load dataset
# ============================================================

def load_data(path: Path) -> pd.DataFrame:
    """
    Load the iFood marketing dataset.
    """

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Please add the CSV file inside the data folder with the name "
            "'ifood_marketing.csv'."
        )

    df = pd.read_csv(path)

    return df


# ============================================================
# 3. Standardize column names
# ============================================================

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to make the analysis easier.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


# ============================================================
# 4. Feature engineering
# ============================================================

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create analytical variables for customer analysis.
    """

    df = df.copy()

    current_year = pd.Timestamp.today().year

    if "year_birth" in df.columns:
        df["age"] = current_year - df["year_birth"]

    spending_columns = [
        "mntwines",
        "mntfruits",
        "mntmeatproducts",
        "mntfishproducts",
        "mntsweetproducts",
        "mntgoldprods"
    ]

    available_spending_columns = [
        col for col in spending_columns if col in df.columns
    ]

    if available_spending_columns:
        df["total_spending"] = df[available_spending_columns].sum(axis=1)

    purchase_columns = [
        "numwebpurchases",
        "numcatalogpurchases",
        "numstorepurchases"
    ]

    available_purchase_columns = [
        col for col in purchase_columns if col in df.columns
    ]

    if available_purchase_columns:
        df["total_purchases"] = df[available_purchase_columns].sum(axis=1)

    if "income" in df.columns:
        df["income_group"] = pd.cut(
            df["income"],
            bins=[0, 30000, 60000, 100000, np.inf],
            labels=[
                "Low income",
                "Middle income",
                "High income",
                "Very high income"
            ]
        )

    if "age" in df.columns:
        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 29, 39, 49, 59, np.inf],
            labels=[
                "Up to 29",
                "30 to 39",
                "40 to 49",
                "50 to 59",
                "60 or more"
            ]
        )

    return df


# ============================================================
# 5. Dataset overview
# ============================================================

def dataset_overview(df: pd.DataFrame) -> None:
    """
    Print a general overview of the dataset.
    """

    print("\n================ DATASET OVERVIEW ================")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isna().sum().sort_values(ascending=False).head(20))

    print("\nFirst rows:")
    print(df.head())


# ============================================================
# 6. Business KPIs
# ============================================================

def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate business KPIs for the portfolio project.
    """

    kpis = {}

    kpis["total_customers"] = len(df)

    if "income" in df.columns:
        kpis["average_income"] = round(df["income"].mean(), 2)

    if "age" in df.columns:
        kpis["average_age"] = round(df["age"].mean(), 2)

    if "total_spending" in df.columns:
        kpis["total_revenue_analyzed"] = round(df["total_spending"].sum(), 2)
        kpis["average_spending_per_customer"] = round(df["total_spending"].mean(), 2)

    if "total_purchases" in df.columns:
        kpis["average_purchases_per_customer"] = round(df["total_purchases"].mean(), 2)

    if "response" in df.columns:
        kpis["campaign_responses"] = int(df["response"].sum())
        kpis["campaign_response_rate_percent"] = round(
            df["response"].mean() * 100,
            2
        )

    kpi_df = pd.DataFrame(
        list(kpis.items()),
        columns=["metric", "value"]
    )

    return kpi_df


# ============================================================
# 7. Save analytical outputs
# ============================================================

def save_outputs(df: pd.DataFrame, kpi_df: pd.DataFrame) -> None:
    """
    Save outputs generated by the analysis.
    """

    treated_data_path = OUTPUT_DIR / "ifood_marketing_treated.csv"
    kpi_path = OUTPUT_DIR / "business_kpis.csv"

    df.to_csv(treated_data_path, index=False)
    kpi_df.to_csv(kpi_path, index=False)

    print("\n================ FILES SAVED ================")
    print(f"Treated dataset: {treated_data_path}")
    print(f"Business KPIs: {kpi_path}")


# ============================================================
# 8. Charts
# ============================================================

def generate_charts(df: pd.DataFrame) -> None:
    """
    Generate simple charts for portfolio documentation.
    """

    if "income" in df.columns:
        plt.figure(figsize=(8, 5))
        df["income"].dropna().hist(bins=30)
        plt.title("Income Distribution")
        plt.xlabel("Income")
        plt.ylabel("Number of customers")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "income_distribution.png")
        plt.close()

    if "total_spending" in df.columns:
        plt.figure(figsize=(8, 5))
        df["total_spending"].dropna().hist(bins=30)
        plt.title("Total Spending Distribution")
        plt.xlabel("Total spending")
        plt.ylabel("Number of customers")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "total_spending_distribution.png")
        plt.close()

    if "age_group" in df.columns and "total_spending" in df.columns:
        spending_by_age = (
            df.groupby("age_group", observed=True)["total_spending"]
            .mean()
            .reset_index()
        )

        plt.figure(figsize=(8, 5))
        plt.bar(
            spending_by_age["age_group"].astype(str),
            spending_by_age["total_spending"]
        )
        plt.title("Average Spending by Age Group")
        plt.xlabel("Age group")
        plt.ylabel("Average spending")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "average_spending_by_age_group.png")
        plt.close()

    if "income_group" in df.columns and "response" in df.columns:
        response_by_income = (
            df.groupby("income_group", observed=True)["response"]
            .mean()
            .mul(100)
            .reset_index()
        )

        plt.figure(figsize=(8, 5))
        plt.bar(
            response_by_income["income_group"].astype(str),
            response_by_income["response"]
        )
        plt.title("Campaign Response Rate by Income Group")
        plt.xlabel("Income group")
        plt.ylabel("Response rate (%)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "response_rate_by_income_group.png")
        plt.close()

    print("\nCharts saved in the outputs folder.")


# ============================================================
# 9. Main execution
# ============================================================

def main() -> None:
    """
    Execute the full exploratory analysis.
    """

    df = load_data(DATA_PATH)

    df = standardize_columns(df)

    dataset_overview(df)

    df = create_features(df)

    kpi_df = calculate_kpis(df)

    print("\n================ BUSINESS KPIS ================")
    print(kpi_df)

    save_outputs(df, kpi_df)

    generate_charts(df)

    print("\nExploratory analysis completed successfully.")


if __name__ == "__main__":
    main()
