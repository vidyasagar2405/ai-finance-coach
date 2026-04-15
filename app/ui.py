import streamlit as st
import pandas as pd
import plotly.express as px

from data import load_transactions
from analysis import analyze_finances
from anomaly import detect_anomalies
from goals import analyze_goal
from chatbot import chat_response

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets")
    st.stop()

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(page_title="Finance Coach", layout="wide")

# -----------------------
# 🎨 ADVANCED THEME CSS
# -----------------------
st.markdown("""
<style>

/* REMOVE GAP ABOVE */
.block-container {
    padding-top: 0 !important;
}
            
/* =========================
🌗 LIGHT + DARK MODE FIX
========================= */

/* Light Mode */
[data-testid="stAppViewContainer"][data-theme="light"] {
    background: #f1f5f9;
}

/* Dark Mode */
[data-testid="stAppViewContainer"][data-theme="dark"] {
    background: radial-gradient(circle at 20% 20%, #0f172a, #020617 60%);
}

/* =========================
🧊 GLASS CARD (ADAPTIVE)
========================= */

.glass-card {
    border-radius: 18px;
    padding: 22px;
    backdrop-filter: blur(12px);
    margin-bottom: 20px;
    position: relative;

    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);

    box-shadow: 
        0 8px 32px rgba(0,0,0,0.5),
        inset 0 0 0.5px rgba(255,255,255,0.2);

    transition: all 0.25s ease;
}

/* 🔥 premium hover */
.glass-card:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 
        0 25px 60px rgba(56,189,248,0.25),
        0 0 20px rgba(56,189,248,0.15);
}

/* ✨ glowing highlight cards */
.highlight-card {
    border: 1px solid rgba(56,189,248,0.5);

    box-shadow:
        0 0 20px rgba(56,189,248,0.25),
        0 10px 40px rgba(56,189,248,0.2);
}


/* =========================
⚡ HOVER (STRONG BUT CLEAN)
========================= */

.glass-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 15px 40px rgba(56,189,248,0.25);
}

/* =========================
🎯 BUTTON
========================= */

.stButton>button {
    border-radius: 12px;
    background: linear-gradient(135deg, #38bdf8, #6366f1);
    color: white;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* =========================
🧭 TABS (RESTORED + BIGGER)
========================= */

div[data-baseweb="tab-list"] {
    gap: 20px;
}

button[data-baseweb="tab"] {
    font-size: 16px;
    padding: 12px 20px;
    border-radius: 12px;
}

/* Selected */
button[aria-selected="true"] {
    background: rgba(56,189,248,0.15);
    color: #38bdf8;
}

/* Hover */
button[data-baseweb="tab"]:hover {
    background: rgba(56,189,248,0.1);
}

/* =========================
📊 CHART GLOW (FIXED)
========================= */

.chart-glow {
    position: relative;
    border-radius: 18px;
    padding: 2px;
    overflow: hidden;
}

/* flowing border light */
.chart-glow::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 18px;
    background: linear-gradient(
        120deg,
        transparent,
        rgba(56,189,248,0.8),
        transparent
    );
    animation: flowBorder 3s linear infinite;
}

/* inner content */
.chart-glow > div {
    position: relative;
    z-index: 1;
    border-radius: 16px;
}

/* smooth flowing animation */
@keyframes flowBorder {
    0% { transform: translateX(-100%) translateY(-100%); }
    50% { transform: translateX(100%) translateY(100%); }
    100% { transform: translateX(-100%) translateY(-100%); }
}

/* =========================
📱 MOBILE FIX
========================= */

@media (max-width: 768px) {
    h1 {font-size: 26px;}
    button[data-baseweb="tab"] {
        font-size: 14px;
        padding: 10px;
    }
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# TITLE
# -----------------------
st.markdown('<div class="sticky-title">', unsafe_allow_html=True)

st.markdown("""
<h1 style="margin:0;">
💰 AI <span style="color:#38bdf8;">Finance Coach</span>
</h1>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.header("User Inputs")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
monthly_income = st.sidebar.number_input("Monthly Income (₹)", value=60000)
target_amount = st.sidebar.number_input("Goal Amount (₹)", value=500000)
months = st.sidebar.number_input("Timeline (months)", value=12)

# 🎯 SET GOAL BUTTON
if st.sidebar.button("🚀 SET GOAL"):
    st.sidebar.success("Goal updated!")

# -----------------------
# CHAT MEMORY
# -----------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------
# MAIN
# -----------------------
if uploaded_file:

    df = load_transactions(uploaded_file)

    analysis = analyze_finances(df)
    anomalies = detect_anomalies(df)
    goal = analyze_goal(df, monthly_income, target_amount, months)

    context = {
        "analysis": analysis,
        "anomalies": anomalies,
        "goal": goal
    }

    # -----------------------
    # AI SUMMARY
    # -----------------------
    summary = chat_response("Summarize my finances", context)

    st.markdown(f"""
    <div class="glass-card highlight-card">
        <h3>🧠 AI Summary</h3>
        <p>{summary}</p>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------
    # TABS
    # -----------------------
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Dashboard", "🚨 Anomalies", "🎯 Goals", "💬 Chat"]
    )

    # ======================
    # DASHBOARD
    # ======================
    with tab1:

        #st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Transactions")
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        total = analysis['insights']['total_spend']
        top = analysis["insights"].get("top_category", {})

        col1.markdown(f"""
        <div class="glass-card highlight-card">
            <h4>Total Spend</h4>
            <h1>₹{total}</h1>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="glass-card highlight-card">
            <h4>Top Category</h4>
            <h1>{top['category']} ({top['percentage']}%)</h1>
        </div>
        """, unsafe_allow_html=True)

        df_cat = pd.DataFrame(analysis["insights"]["category_breakdown"])

        max_row = df_cat.loc[df_cat["amount"].idxmax()]
        min_row = df_cat.loc[df_cat["amount"].idxmin()]

        col1, col2 = st.columns(2)

        col1.markdown(f"""
        <div class="glass-card strong-border">
            <h4>Least Spending</h4>
            <p>{min_row['category']} — ₹{min_row['amount']}</p>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="glass-card strong-border">
            <h4>Highest Spending</h4>
            <p>{max_row['category']} — ₹{max_row['amount']}</p>
        </div>
        """, unsafe_allow_html=True)

        if top["percentage"] > 40:
            st.markdown(f"""
            <div class="glass-card strong-border">
                <h4>⚠ Overspending Alert</h4>
                <p>You spend {top['percentage']}% on {top['category']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="chart-glow">', unsafe_allow_html=True)
            fig1 = px.pie(df_cat, names="category", values="amount", hole=0.5)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chart-glow">', unsafe_allow_html=True)
            fig2 = px.bar(df_cat, x="category", y="amount")
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ======================
    # ANOMALIES
    # ======================
    with tab2:

        #st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        if anomalies["transaction_anomalies"]:
            st.dataframe(pd.DataFrame(anomalies["transaction_anomalies"]))
        else:
            st.success("No anomalies")

        for spike in anomalies["category_spikes"]:
            st.warning(spike)

        st.markdown('</div>', unsafe_allow_html=True)

    # ======================
    # GOALS
    # ======================
    with tab3:

        plan = goal["goal_plan"]

        col1, col2, col3 = st.columns(3)

        col1.metric("Required / Month", f"₹{plan['required_per_month']}")
        col2.metric("Current Savings", f"₹{plan['current_savings']}")
        col3.metric("Gap", f"₹{plan['gap']}")

        st.progress(min(plan["current_savings"]/target_amount, 1.0))

        if plan["status"] == "on_track":
            st.success("On track")
        else:
            st.error("Behind goal")

        # 🎯 BUTTON INSIDE TAB
        if st.button("🎯 Adjust Goal"):
            st.success("Goal updated!")

    # ======================
    # CHAT
    # ======================
    with tab4:

        for chat in st.session_state.chat_history:

            st.markdown(f"""
            <div class="glass-card">
                <b>You:</b><br>{chat['user']}
                <br><br>
                <b>Coach:</b><br>{chat['bot']}
            </div>
            """, unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):

            user_input = st.text_input("Ask something...")
            submit = st.form_submit_button("Send")

            if submit and user_input:

                response = chat_response(user_input, context)

                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": response
                })

                st.rerun()

else:
    st.info("Upload CSV to start")