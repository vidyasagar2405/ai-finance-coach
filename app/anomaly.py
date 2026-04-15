import pandas as pd


# 🔹 1. Transaction-level anomaly detection
def detect_transaction_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flags unusually high transactions using statistical threshold
    """
    if df.empty:
        return pd.DataFrame()

    mean = df["amount"].mean()
    std = df["amount"].std()

    threshold = mean + (2 * std)

    anomalies = df[df["amount"] > threshold].copy()
    anomalies["anomaly_reason"] = "Unusually high transaction"

    return anomalies


# 🔹 2. Category-level anomaly detection
def detect_category_spikes(df: pd.DataFrame) -> list:
    """
    Detects categories with unusually high total spend
    """
    if df.empty:
        return []

    category_spend = df.groupby("category")["amount"].sum()

    mean = category_spend.mean()
    std = category_spend.std()

    threshold = mean + (1.5 * std)

    spikes = []

    for category, amount in category_spend.items():
        if amount > threshold:
            spikes.append(
                f"{category.capitalize()} spending is unusually high (₹{amount})"
            )

    return spikes


# 🔹 3. Combine anomalies
def detect_anomalies(df: pd.DataFrame) -> dict:
    """
    Main anomaly detection function
    """
    txn_anomalies = detect_transaction_anomalies(df)
    category_spikes = detect_category_spikes(df)

    return {
        "transaction_anomalies": txn_anomalies.to_dict(orient="records"),
        "category_spikes": category_spikes
    }


# 🔹 Test locally
if __name__ == "__main__":
    from data import load_transactions
    from pathlib import Path
    from pprint import pprint

    ROOT = Path(__file__).resolve().parents[1]
    sample_path = ROOT / "data" / "sample.csv"

    df = load_transactions(sample_path)

    result = detect_anomalies(df)
    pprint(result)