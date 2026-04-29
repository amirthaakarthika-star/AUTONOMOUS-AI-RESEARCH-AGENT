import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.graph import run_research_graph
from src.report_generator import save_markdown_report, markdown_to_pdf_bytes,markdown_to_pdf_bytes
from src.utils import ensure_output_dir

load_dotenv()

st.set_page_config(page_title="Autonomous AI Research Agent", layout="wide")


st.markdown(
    """
    <style>
        .hero-box {
            padding: 2rem;
            border-radius: 20px;
            background: linear-gradient(135deg, rgba(8,15,52,0.95), rgba(18,56,88,0.92));
            border: 1px solid rgba(125, 211, 252, 0.25);
            box-shadow: 0 10px 30px rgba(0,0,0,0.18);
            margin-bottom: 1.5rem;
            color: white;
        }
        .hero-title {
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 0.3rem;
        }
        .hero-subtitle {
            font-size: 1rem;
            opacity: 0.9;
        }
    </style>
    <div class="hero-box">
        <div class="hero-title">Autonomous AI Research Agent</div>
        <div class="hero-subtitle">
            LangGraph-powered live web research for competitor analysis, market research, and trend reports.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if "latest_report" not in st.session_state:
    st.session_state.latest_report = ""
if "latest_sources" not in st.session_state:
    st.session_state.latest_sources = []
if "latest_plan" not in st.session_state:
    st.session_state.latest_plan = ""
if "latest_findings" not in st.session_state:
    st.session_state.latest_findings = []
if "latest_saved_path" not in st.session_state:
    st.session_state.latest_saved_path = ""

with st.sidebar:
    st.header("Research Settings")

    report_type = st.selectbox(
        "Select Report Type",
        ["Competitor Analysis", "Market Research", "Trend Analysis"],
    )

    max_results = st.slider("Search Results Per Query", 3, 8, 5)
    show_plan = st.checkbox("Show research plan", value=True)
    show_findings = st.checkbox("Show findings", value=False)

    st.markdown("---")
    st.markdown("**Required API Keys**")
    st.caption("Set `GROQ_API_KEY` and `TAVILY_API_KEY` in your `.env` file.")

topic = st.text_area(
    "Enter research topic",
    placeholder="Example: Analyze top AI interview platforms in Singapore, compare features, pricing, and target users.",
    height=120,
)

run_button = st.button("Run Research", type="primary", use_container_width=True)

if run_button:
    if not os.getenv("GROQ_API_KEY"):
        st.error("Missing GROQ_API_KEY in .env")
        st.stop()

    if not os.getenv("TAVILY_API_KEY"):
        st.error("Missing TAVILY_API_KEY in .env")
        st.stop()

    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    with st.spinner("Running autonomous research workflow..."):
        result = run_research_graph(
            topic=topic.strip(),
            report_type=report_type,
            max_results=max_results,
        )

        st.session_state.latest_report = result["final_report"]
        st.session_state.latest_sources = result["sources"]
        st.session_state.latest_plan = result["research_plan"]
        st.session_state.latest_findings = result["findings"]

        ensure_output_dir("outputs")
        saved_path = save_markdown_report(
            report=result["final_report"],
            topic=topic.strip(),
            output_dir="outputs",
        )
        st.session_state.latest_saved_path = saved_path

if st.session_state.latest_report:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Generated Report")
        st.markdown(st.session_state.latest_report)

    with col2:
        st.subheader("Actions")
        pdf_bytes = markdown_to_pdf_bytes(st.session_state.latest_report, st.session_state.get("latest_topic", "report"))
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="research_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

        if st.session_state.latest_saved_path:
            st.success(f"Saved locally: {Path(st.session_state.latest_saved_path).name}")

    if show_plan:
        with st.expander("Research Plan", expanded=False):
            st.write(st.session_state.latest_plan)

    if show_findings:
        with st.expander("Research Findings", expanded=False):
            for i, finding in enumerate(st.session_state.latest_findings, start=1):
                st.markdown(f"**Finding {i}:** {finding}")

    with st.expander("Sources", expanded=False):
        for source in st.session_state.latest_sources:
            st.markdown(f"- [{source['title']}]({source['url']})")


