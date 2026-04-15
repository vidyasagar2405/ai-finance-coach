import pandas as pd


# 🔹 1. Monthly savings capacity
def calculate_monthly_savings(df: pd.DataFrame, monthly_income: float) -> float:
    """
    Estimate how much user can save monthly
    """
    total_spend = df["amount"].sum()

    # assuming df is 1 month data
    savings = monthly_income - total_spend

    return max(savings, 0)


# 🔹 2. Goal planning
def create_goal_plan(
    target_amount: float,
    months: int,
    monthly_income: float,
    df: pd.DataFrame
) -> dict:
    """
    Create a savings plan for a goal
    """

    required_per_month = target_amount / months
    current_savings = calculate_monthly_savings(df, monthly_income)

    gap = required_per_month - current_savings

    if gap <= 0:
        status = "on_track"
    else:
        status = "behind"

    return {
        "target_amount": target_amount,
        "months": months,
        "required_per_month": round(required_per_month, 2),
        "current_savings": round(current_savings, 2),
        "gap": round(gap, 2),
        "status": status
    }


# 🔹 3. Suggest improvements
def goal_recommendations(goal_plan: dict) -> list:
    """
    Suggest how to achieve the goal
    """

    recs = []

    if goal_plan["status"] == "on_track":
        recs.append("You're on track! Maintain your current spending habits.")
        return recs

    gap = goal_plan["gap"]

    recs.append(
        f"You need an additional ₹{gap:.0f}/month to meet your goal."
    )

    recs.append(
        "Consider reducing discretionary spending (shopping, dining, subscriptions)."
    )

    recs.append(
        "Increase savings by setting auto-debits or cutting non-essential expenses."
    )

    return recs


# 🔹 4. Combine everything
def analyze_goal(
    df: pd.DataFrame,
    monthly_income: float,
    target_amount: float,
    months: int
) -> dict:
    """
    Full goal analysis
    """

    plan = create_goal_plan(
        target_amount,
        months,
        monthly_income,
        df
    )

    recommendations = goal_recommendations(plan)

    return {
        "goal_plan": plan,
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

    result = analyze_goal(
        df,
        monthly_income=30000,
        target_amount=500000,
        months=12
    )

    pprint(result)