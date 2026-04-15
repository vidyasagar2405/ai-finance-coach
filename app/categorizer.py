import json
from pathlib import Path
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import streamlit as st

def load_cate():
    path = Path(__file__).resolve().parent.parent / "data" / "categories.json"
    with open(path, "r") as f:
        return json.load(f)

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=st.secrets["GROQ_API_KEY"]
)


@st.cache_data
def classify_cached(desc, categories):
    return classify_with_schema(desc, categories)


def classify_with_schema(description: str, categories: dict):

    # Format categories nicely
    cat_text = ""
    for cat, subs in categories.items():
        cat_text += f"{cat}: {', '.join(subs)}\n"

    prompt = f"""
You are a strict financial classifier.

You MUST choose:
- One category
- One subcategory

ONLY from this list:

{cat_text}

Rules:
- Do NOT invent new categories
- If unsure → choose "others" and "general"

Output EXACTLY like:
category: <category>
subcategory: <subcategory>

Transaction:
{description}
"""

    response = model.invoke(prompt).content.strip()

    try:
        lines = response.split("\n")
        category = lines[0].split(":")[1].strip().lower()
        subcategory = lines[1].split(":")[1].strip().lower()
    except:
        return "others", "uncategorized"

    # ✅ Validation
    if category not in categories:
        return "others", "uncategorized"

    if subcategory not in categories.get(category, []):
        subcategory = "uncategorized"

    return category, subcategory