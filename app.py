
import logging
from pathlib import Path

import pandas as pd
import streamlit as st
from agent import ask_agent

# --------------------------------------------------
# Configuration
# --------------------------------------------------
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "sales_data.csv"
SOP_FILE = BASE_DIR / "data" / "sales_sop.txt"
LOG_FILE = BASE_DIR / "app.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="METRO | AI Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Premium UI / UX Styling
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080d19;
    --panel: #111a2b;
    --panel2: #151f33;
    --border: rgba(148,163,184,.16);
    --text: #f1f5f9;
    --muted: #94a3b8;
    --cyan: #38bdf8;
    --violet: #a78bfa;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #142846 0%, transparent 38%),
        radial-gradient(ellipse at 90% 5%, #251b45 0%, transparent 30%),
        var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10192a, #090f1d);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] * {
    color: var(--text);
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 32px;
    border: 1px solid rgba(56,189,248,.25);
    border-radius: 24px;
    background: linear-gradient(115deg, #142b49 0%, #172039 52%, #28204a 100%);
    box-shadow: 0 18px 60px rgba(0,0,0,.20);
    animation: fadeUp .7s ease both;
}

.hero:after {
    content: "";
    position: absolute;
    width: 250px;
    height: 250px;
    right: -65px;
    top: -100px;
    border-radius: 50%;
    background: rgba(56,189,248,.13);
    filter: blur(8px);
}

.eyebrow {
    color: #7dd3fc;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero h1 {
    color: white !important;
    font-size: clamp(28px, 4vw, 43px) !important;
    font-weight: 800 !important;
    margin: 12px 0 8px !important;
    line-height: 1.15 !important;
}

.hero p {
    color: #cbd5e1;
    font-size: 15px;
    max-width: 700px;
    line-height: 1.8;
}

.status-pill {
    display: inline-block;
    margin-top: 12px;
    padding: 7px 12px;
    border: 1px solid rgba(74,222,128,.25);
    border-radius: 30px;
    background: rgba(34,197,94,.10);
    color: #86efac;
    font-size: 12px;
    font-weight: 700;
}

.section-title {
    font-size: 21px;
    font-weight: 750;
    color: #f8fafc;
    margin: 24px 0 14px;
}

.metric-card {
    padding: 22px;
    min-height: 145px;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: linear-gradient(145deg, rgba(21,31,51,.98), rgba(13,21,36,.98));
    transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
    animation: fadeUp .6s ease both;
}

.metric-card:hover {
    transform: translateY(-5px);
    border-color: rgba(56,189,248,.5);
    box-shadow: 0 12px 30px rgba(0,0,0,.20);
}

.metric-label {
    color: #9fb0c8;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    margin-top: 14px;
    color: #f8fafc;
    font-size: clamp(22px, 2.4vw, 32px);
    font-weight: 800;
    letter-spacing: -.7px;
    overflow-wrap: anywhere;
}

.metric-note {
    color: #7dd3fc;
    font-size: 12px;
    margin-top: 7px;
}

.panel {
    padding: 20px;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: rgba(17,26,43,.82);
}

div[data-testid="stChatMessage"] {
    background: rgba(21,31,51,.82);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 16px;
    margin-bottom: 12px;
    animation: fadeUp .35s ease both;
}

div[data-testid="stChatInput"] {
    border-color: rgba(56,189,248,.45) !important;
    border-radius: 15px !important;
}

.stButton > button {
    border: 1px solid rgba(56,189,248,.30);
    border-radius: 12px;
    background: linear-gradient(100deg, #0e7490, #6d28d9);
    color: white;
    font-weight: 700;
    transition: all .2s ease;
}

.stButton > button:hover {
    border-color: #7dd3fc;
    transform: translateY(-2px);
    box-shadow: 0 7px 22px rgba(56,189,248,.17);
    color: white;
}

div[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    background: rgba(17,26,43,.60);
}

div[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

.footer {
    color: #64748b;
    text-align: center;
    font-size: 12px;
    padding: 25px 0 5px;
    border-top: 1px solid var(--border);
    margin-top: 30px;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def money(value):
    return f"₹{value:,.0f}"


def metric_card(label, value, note, icon):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{icon} &nbsp; {label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_sales_data():
    if not DATA_FILE.exists():
        return pd.DataFrame()
    return pd.read_csv(DATA_FILE)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown("## ◈ METRO AI")
    st.caption("SALES INTELLIGENCE PLATFORM")
    st.divider()

    st.markdown("### Navigation")
    st.markdown("📊  Sales dashboard")
    st.markdown("🤖  AI assistant")
    st.markdown("📚  SOP knowledge base")

    st.divider()
    st.markdown("### Platform")
    st.markdown("🟢 Agent interface")
    st.markdown("🔗 LangGraph + Groq")
    st.markdown("📁 CSV + SOP documents")

    st.divider()
    if st.button("🗑️ Clear chat history", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.caption("METRO Sales Assistant · Demo")


# --------------------------------------------------
# Hero Header
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">METRO • AI-POWERED BUSINESS INTELLIGENCE</div>
    <h1>Sales Intelligence, <span style="color:#7dd3fc;">Reimagined.</span></h1>
    <p>
        Explore sales performance, understand regional trends, and ask questions
        about business data and standard operating procedures using your AI assistant.
    </p>
    <span class="status-pill">● Dashboard ready</span>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Sales Dashboard
# --------------------------------------------------
st.markdown('<div class="section-title">📊 Executive Overview</div>',
            unsafe_allow_html=True)

df = pd.DataFrame()

try:
    df = load_sales_data()

    required_columns = {"product", "region", "sales"}
    if not df.empty and required_columns.issubset(df.columns):
        df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
        df = df.dropna(subset=["sales"])

        total_sales = df["sales"].sum()
        total_records = len(df)
        product_count = df["product"].nunique()
        region_count = df["region"].nunique()

        k1, k2, k3, k4 = st.columns(4, gap="medium")

        with k1:
            metric_card("Total Sales", money(total_sales),
                        "Across available records", "💰")

        with k2:
            metric_card("Sales Records", f"{total_records:,}",
                        "Rows analysed", "📈")

        with k3:
            metric_card("Products", f"{product_count:,}",
                        "Distinct products", "📦")

        with k4:
            metric_card("Regions", f"{region_count:,}",
                        "Distinct sales regions", "🌐")

        # Charts
        st.markdown(
            '<div class="section-title">📈 Performance Analytics</div>',
            unsafe_allow_html=True,
        )

        left, right = st.columns(2, gap="large")

        with left:
            with st.container(border=True):
                st.markdown("#### Product-wise Sales")
                product_sales = (
                    df.groupby("product")["sales"]
                    .sum()
                    .sort_values(ascending=False)
                )
                st.bar_chart(product_sales, height=320)

        with right:
            with st.container(border=True):
                st.markdown("#### Region-wise Sales")
                region_sales = (
                    df.groupby("region")["sales"]
                    .sum()
                    .sort_values(ascending=False)
                )
                st.bar_chart(region_sales, height=320)

        # Insights
        st.markdown(
            '<div class="section-title">✨ Quick Insights</div>',
            unsafe_allow_html=True,
        )

        i1, i2 = st.columns(2, gap="medium")

        with i1:
            best_product = df.groupby("product")["sales"].sum().idxmax()
            best_product_sales = df.groupby("product")["sales"].sum().max()
            st.markdown(
                f"""
                <div class="panel">
                    <div class="metric-label">🏆 TOP-PERFORMING PRODUCT</div>
                    <div class="metric-value" style="font-size:24px;">
                        {best_product}
                    </div>
                    <div class="metric-note">
                        Sales: {money(best_product_sales)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with i2:
            best_region = df.groupby("region")["sales"].sum().idxmax()
            best_region_sales = df.groupby("region")["sales"].sum().max()
            st.markdown(
                f"""
                <div class="panel">
                    <div class="metric-label">🌍 TOP-PERFORMING REGION</div>
                    <div class="metric-value" style="font-size:24px;">
                        {best_region}
                    </div>
                    <div class="metric-note">
                        Sales: {money(best_region_sales)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with st.expander("🔎 View sales data"):
            st.dataframe(df, use_container_width=True, hide_index=True)

    else:
        st.warning(
            "Sales data is missing or does not contain the expected "
            "columns: product, region and sales."
        )

except Exception as exc:
    logger.exception("Dashboard loading failed")
    st.warning(f"Dashboard data could not be loaded: {exc}")


# --------------------------------------------------
# AI Assistant
# --------------------------------------------------
st.markdown(
    '<div class="section-title">🤖 Ask the METRO AI Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown("""
<div class="panel">
    <b style="color:#7dd3fc;">Your business copilot</b>
    <p style="color:#94a3b8; margin-bottom:0;">
        Ask about sales figures, top-performing products, regions,
        or the return policy documented in the sales SOP.
    </p>
</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Suggested prompts
st.caption("TRY A QUESTION")

suggestions = [
    "What is the return period for a product?",
    "What is the return policy for damaged products?",
    "Which product has the highest sales?",
]

suggestion_cols = st.columns(3)

for index, prompt in enumerate(suggestions):
    with suggestion_cols[index]:
        if st.button(prompt, key=f"suggestion_{index}",
                     use_container_width=True):
            st.session_state.pending_question = prompt

# Previous conversation
for item in st.session_state.chat_history:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

question = st.chat_input("Ask about sales or SOP documents...")

if "pending_question" in st.session_state:
    question = st.session_state.pop("pending_question")

if question:
    st.session_state.chat_history.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Analysing your question..."):
            try:
                logger.info("Agent request started")
                answer = ask_agent(question)

                if answer is None or not str(answer).strip():
                    answer = (
                        "I couldn't generate an answer. "
                        "Please try rephrasing your question."
                    )

                answer = str(answer)
                st.markdown(answer)
                logger.info("Agent request completed")

            except Exception:
                logger.exception("Agent request failed")
                answer = (
                    "Sorry, the AI assistant encountered an error. "
                    "Please try again. If the issue continues, check "
                    "the application logs."
                )
                st.error(answer)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )


# --------------------------------------------------
# Knowledge sources and footer
# --------------------------------------------------
with st.expander("📚 Knowledge sources & project details"):
    st.markdown(f"""
    - **Sales data:** `{DATA_FILE.relative_to(BASE_DIR)}`
    - **Sales SOP:** `{SOP_FILE.relative_to(BASE_DIR)}`
    - **Agent framework:** LangGraph
    - **LLM provider:** Groq
    - **Interface:** Streamlit
    """)

st.markdown("""
<div class="footer">
    METRO AI Sales Assistant · Built with Streamlit, LangGraph and Python
    <br>Interactive demo for sales analytics and SOP question answering
</div>
""", unsafe_allow_html=True)
