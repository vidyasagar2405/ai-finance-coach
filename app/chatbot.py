import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Groq Model (fast + free)
model = ChatGroq(
    model="llama-3.3-70b-versatile",  # best option
    temperature=0.2,
)


# Format structured context
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
        formatted_context = format_context(context)
        q = question.lower()

        planning_keywords = [
            "plan", "roadmap", "monthly", "save", "goal",
            "buy house", "buy car", "retire", "timeline",
            "actionable", "strategy"
        ]

        is_planning = any(word in q for word in planning_keywords)

        if is_planning:
            instructions = """
                        You are an expert personal finance planner.

                        Create a personalized actionable plan.

                        Instructions:
                        - Use the provided financial data.
                        - Give exact monthly targets.
                        - Use bullet points.
                        - Include:
                        1. Goal summary
                        2. Monthly savings needed
                        3. Spending cuts by category
                        4. Month-by-month roadmap
                        5. Risks to avoid
                        6. Final recommendation
                        - Minimum 200 words.
                        - Be practical and realistic.
                        """
        else:
            instructions = """
                        You are an expert financial coach.

                        Instructions:
                        - Answer only finance-related questions.
                        - Use data if relevant.
                        - If greeting, reply naturally.
                        - Be concise.
                        - Use bullets when useful.
                        - 3 to 6 lines max.
                        """

        prompt = f"""
                        Financial Context:
                        {formatted_context}

                        User Question:
                        {question}

                        {instructions}
                        """

        response = model.invoke(prompt)
        return response.content

    except Exception as e:
        return f"Error: {str(e)}"

    except Exception as e:
        return f"Error: {str(e)}"
