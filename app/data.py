import pandas as pd
import json
import re
from pathlib import Path
from typing import Any
from categorizer import classify_with_schema, load_cate, classify_cached

# Path setup
ROOT = Path(__file__).resolve().parents[1]
CATEGORIES_PATH = ROOT / "data" / "categories.json"


# 🔹 Load categories.json
def load_categories() -> dict[Any, Any]:
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        categories = json.load(f)

    mapping: dict[Any, Any] = {}
    for category, subcats in categories.items():
        for sub in subcats:
            mapping[sub] = category

    return mapping


# 🔹 Normalize text
def normalize_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# 🔹 Categorize description
def categorize(description: str, mapping: dict[Any, Any]) -> tuple[Any, Any]:
    desc = normalize_text(description)

    for key in mapping:
        if key in desc:
            return mapping[key], key

    return "Unknown", "uncategorized"


# 🔹 Main function
def load_transactions(file):
    df = pd.read_csv(file)

    # Normalize column names
    df.columns = [c.lower().strip() for c in df.columns]

    # Validate required columns
    required_cols = ["date", "amount", "description"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}. CSV must contain: {required_cols}"
        )

    # Convert amount
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    # Load mapping
    mapping = load_categories()

    # Rule-based categorization
    categories_series = df["description"].apply(lambda x: categorize(x, mapping))
    df["category"] = categories_series.apply(lambda x: x[0])
    df["subcategory"] = categories_series.apply(lambda x: x[1])

    # LLM fallback (FIXED LOCATION)
    categories_json = load_cate()

    for i, row in df.iterrows():
        if row["category"] in ["Unknown", "", None] or str(row["category"]).lower() == "others":
            cat, sub = classify_cached(row["description"], categories_json)
            df.at[i, "category"] = cat
            df.at[i, "subcategory"] = sub

    return df


# 🔹 Test locally
if __name__ == "__main__":
    sample_path = ROOT / "data" / "sample.csv"
    df = load_transactions(sample_path)
    print(df.head())