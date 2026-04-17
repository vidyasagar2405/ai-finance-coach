# AI-Powered Finance Coach

An intelligent personal finance assistant that transforms transaction data into actionable insights using AI and Large Language Models (LLMs).

The application helps users analyze spending patterns, detect anomalies, track financial goals, and receive personalized recommendations through a conversational chatbot interface.

---

## Features

* Upload transaction data using CSV files
* Automated transaction categorization (Rule-based + AI)
* Interactive dashboard with charts and spending insights
* Anomaly detection for unusual transactions and overspending
* Goal planning and progress tracking
* 🤖 AI chatbot for personalized financial guidance
* ☁️ Web deployment using Streamlit Community Cloud

---

## Tech Stack

### Core Development

* Python
* Pandas
* Streamlit
* Plotly

### AI / Machine Learning

* LangChain
* Groq API
* LLaMA Models

### Deployment & Version Control

* GitHub
* Streamlit Community Cloud

---

## 📁 Project Structure

```text
AI-Finance-Coach/
│── app/
│   ├── ui.py
│   ├── data.py
│   ├── categorizer.py
│   ├── analysis.py
│   ├── anomaly.py
│   ├── goals.py
│   └── chatbot.py
│
│── data/
│   ├── sample.csv
│   └── categories.json
│
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### 5. Run Application

```bash
streamlit run app/ui.py
```

---

## How It Works

1. Upload transaction CSV file
2. Data is cleaned and categorized
3. Spending analysis is generated
4. Anomalies are detected
5. Goal progress is evaluated
6. AI chatbot provides recommendations

---

## Future Scope

* Bank API integration
* Real-time alerts
* Mobile application
* Advanced ML anomaly detection
* Dual-mode API access

---

## 🤝 Contributing

Contributions, ideas, and improvements are welcome.