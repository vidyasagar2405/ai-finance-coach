import os
from langchain_groq import ChatGroq
import streamlit as st

# ✅ Groq Model (fast + free)
model = ChatGroq(
    model="llama-3.3-70b-versatile",  # best option
    temperature=0.2,
    api_key = st.secrets["GROQ_API_KEY"]
)


# 🔹 Format structured context
def format_context(context: dict) -> str:
    analysis = context.get("analysis", {})
    anomalies = context.get("anomalies", {})
    goal = context.get("goal", {})
    history = context.get("history", [])

    monthly_income = context.get("monthly_income", 0)
    target_amount = context.get("target_amount", 0)
    months = context.get("months", 0)

    if analysis:
        insights = analysis.get("insights", {})
        recommendations = analysis.get("recommendations", [])

        total = insights.get("total_spend", 0)
        top = insights.get("top_category", {})
        breakdown = insights.get("category_breakdown", [])

        breakdown_text = "\n".join(
            [
                f"- {item['category']}: ₹{item['amount']} ({item.get('percentage', 0)}%)"
                for item in breakdown
            ]
        )

        rec_text = "\n".join([f"- {r}" for r in recommendations])

        anomaly_text = ""
        txn = anomalies.get("transaction_anomalies", [])
        spikes = anomalies.get("category_spikes", [])

        if txn:
            anomaly_text += "Unusual Transactions Detected\n"
        if spikes:
            anomaly_text += "\n".join([f"- {s}" for s in spikes])

        goal_text = ""
        plan = goal.get("goal_plan", {})
        if plan:
            goal_text = f"""
Goal Status:
- Target: ₹{target_amount} over {months} months
- Required per month: ₹{plan.get("required_per_month")}
- Current savings: ₹{plan.get("current_savings")}
- Gap: ₹{plan.get("gap")}
- Status: {plan.get("status")}
"""
    else:
        total = 0
        top = {}
        breakdown_text = "No data"
        rec_text = "Upload transactions first"
        anomaly_text = ""
        goal_text = f"""
Goal Parameters:
- Monthly Income: ₹{monthly_income}
- Target Amount: ₹{target_amount}
- Timeline: {months} months
"""

    history_text = ""
    if history:
        history_text = "\nConversation History:\n"
        for h in history[-3:]:
            history_text += f"User: {h['user']}\nCoach: {h['bot']}\n"

    formatted = f"""
Financial Summary:
- Total Spend: ₹{total}
- Top Category: {top.get("category", "N/A")} ({top.get("percentage", 0)}%)

Category Breakdown:
{breakdown_text}

System Recommendations:
{rec_text}

{anomaly_text}

{goal_text}

{history_text}
"""

    return formatted


# 🔹 Chat function
def chat_response(question: str, context: dict) -> str:
    try:
        analysis = context.get("analysis")
        anomalies = context.get("anomalies")
        goal = context.get("goal")
        history = context.get("history", [])
        monthly_income = context.get("monthly_income", 0)
        target_amount = context.get("target_amount", 0)
        months = context.get("months", 0)

        chat_context = {
            "analysis": analysis,
            "anomalies": anomalies,
            "goal": goal,
            "history": history,
            "monthly_income": monthly_income,
            "target_amount": target_amount,
            "months": months,
        }

        formatted_context = format_context(chat_context)

        prompt = f"""
You are an expert financial coach.

Analyze the user's financial data and answer intelligently.

{formatted_context}

Focus on the question, 
if the Quesition required the analysis then only take the 'formatted context'
if not answer directly.
Only answer to question's that were related to the finance, if user ask out of the domain replay politly like
"I'm only a Finance assistance, ask queries related to finance."
if question is like a greating or a sendoff type message, respond accordingly.

User Question:
{question}

Instructions:
- Answer based on the question of the user.
- If formatted_context is not required, Then use your knowledge to answer.
- Be data-driven
- Use numbers & percentages
- Identify overspending
- Consider goals & anomalies
- Give actionable advice
- Avoid repeating same answer
- Keep it concise (3-5 lines)
"""

        response = model.invoke(prompt)
        return response.content

    except Exception as e:
        return f"Error: {str(e)}"
