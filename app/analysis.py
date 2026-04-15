import pandas as pd


# 🔹 1. Category-wise spending with percentage
def get_category_spend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns total spend per category with percentage contribution
    """
    category_spend = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    total = category_spend["amount"].sum()

    if total > 0:
        category_spend["percentage"] = (
            category_spend["amount"] / total * 100
        ).round(2)
    else:
        category_spend["percentage"] = 0

    return category_spend


# 🔹 2. Total spend
def get_total_spend(df: pd.DataFrame) -> float:
    return float(df["amount"].sum())


# 🔹 3. Top category
def get_top_category(category_spend: pd.DataFrame) -> dict:
    if category_spend.empty:
        return {}

    top = category_spend.iloc[0]

    return {
        "category": top["category"],
        "amount": float(top["amount"]),
        "percentage": float(top["percentage"])
    }


# 🔹 4. Generate insights
def generate_insights(df: pd.DataFrame) -> dict:
    category_spend = get_category_spend(df)
    total = get_total_spend(df)
    top_category = get_top_category(category_spend)

    insights = {
        "total_spend": total,
        "top_category": top_category,
        "category_breakdown": category_spend.to_dict(orient="records")
    }

    return insights


# 🔹 5. Smart budget recommendation (category-agnostic)
def budget_recommendation(category_spend: pd.DataFrame) -> list:
    recommendations = []

    if category_spend.empty:
        return ["No spending data available"]

    for _, row in category_spend.iterrows():
        category = row["category"]
        percentage = row["percentage"]

        # Generic scalable rules

        if percentage > 50:
            recommendations.append(
                f"{category.capitalize()} dominates your spending ({percentage:.1f}%). Consider reducing it."
            )

        elif percentage > 30:
            recommendations.append(
                f"{category.capitalize()} is a major expense ({percentage:.1f}%). Monitor and optimize it."
            )

        elif percentage < 5:
            recommendations.append(
                f"{category.capitalize()} spending is minimal ({percentage:.1f}%)."
            )

    if not recommendations:
        recommendations.append("Your spending distribution looks balanced.")

    return recommendations


# 🔹 6. Main analysis function (for chatbot)
def analyze_finances(df: pd.DataFrame) -> dict:
    category_spend = get_category_spend(df)

    insights = {
        "total_spend": get_total_spend(df),
        "top_category": get_top_category(category_spend),
        "category_breakdown": category_spend.to_dict(orient="records")
    }

    recommendations = budget_recommendation(category_spend)

    return {
        "insights": insights,
        "recommendations": recommendations
    }


# 🔹 Test locally
if __name__ == "__main__":
    from data import load_transactions
    from pathlib import Path
    from pprint import pprint

    ROOT = Path(__file__).resolve().parents[1]
    sample_path = ROOT / "data" / "sample.csv"

    df = load_transactions(sample_path)

    result = analyze_finances(df)
    pprint(result)