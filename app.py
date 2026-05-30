"""
PersuasionLens — Streamlit Web App

Run with: streamlit run app.py
"""

import streamlit as st
import json
from analyzer import analyze, compare

st.set_page_config(page_title="PersuasionLens", page_icon="🔍", layout="wide")

st.title("🔍 PersuasionLens")
st.caption("AI-powered writing persuasiveness analyzer — built on persuasion science")

# --- Sidebar ---
st.sidebar.header("Settings")
context = st.sidebar.selectbox(
    "What kind of text is this?",
    [
        "cold outreach email",
        "LinkedIn post",
        "product pitch",
        "job application cover letter",
        "sales copy",
        "blog post introduction",
        "fundraising pitch",
        "general",
    ],
)

mode = st.sidebar.radio("Mode", ["Analyze", "Compare A/B"])

# --- Main area ---
if mode == "Analyze":
    text = st.text_area(
        "Paste your text below:",
        height=200,
        placeholder="e.g., Hi, I saw your company is hiring for ML engineers...",
    )

    if st.button("Analyze Persuasiveness", type="primary"):
        if not text.strip():
            st.warning("Please paste some text to analyze.")
        else:
            with st.spinner("Analyzing with Claude..."):
                try:
                    result = analyze(text, context)
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.stop()

            # --- Display results ---
            st.divider()

            # Overall score
            col1, col2 = st.columns([1, 3])
            with col1:
                score = result["overall_score"]
                color = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"
                st.metric("Overall Score", f"{score}/10", delta=None)
            with col2:
                st.info(result["summary"])

            # Dimension scores
            st.subheader("Dimension Breakdown")
            dims = result["dimensions"]
            cols = st.columns(3)
            for i, (dim, data) in enumerate(dims.items()):
                with cols[i % 3]:
                    name = dim.replace("_", " ").title()
                    st.metric(name, f"{data['score']}/10")
                    st.progress(data["score"] / 10)
                    st.caption(data["evidence"][:150])

            # Techniques & weaknesses
            col_left, col_right = st.columns(2)
            with col_left:
                st.subheader("Techniques Detected")
                for t in result.get("techniques_detected", []):
                    st.markdown(f"- ✅ {t}")
            with col_right:
                st.subheader("Weaknesses")
                for w in result.get("weaknesses", []):
                    st.markdown(f"- ⚠️ {w}")

            # Suggestions
            st.subheader("Actionable Suggestions")
            for s in result.get("suggestions", []):
                st.markdown(f"→ {s}")

            # Rewrite
            st.subheader("Suggested Rewrite")
            st.success(result.get("rewrite", "N/A"))

            # Raw JSON (collapsible)
            with st.expander("View raw JSON response"):
                st.json(result)

elif mode == "Compare A/B":
    col_a, col_b = st.columns(2)
    with col_a:
        text_a = st.text_area("Version A:", height=200, key="a")
    with col_b:
        text_b = st.text_area("Version B:", height=200, key="b")

    if st.button("Compare", type="primary"):
        if not text_a.strip() or not text_b.strip():
            st.warning("Please paste text in both fields.")
        else:
            with st.spinner("Analyzing both versions..."):
                try:
                    result = compare(text_a, text_b, context)
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.stop()

            st.divider()

            winner = result["winner"]
            st.success(
                f"**Version {winner} wins** by {result['score_delta']} points "
                f"({result['version_a']['overall_score']}/10 vs {result['version_b']['overall_score']}/10)"
            )

            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"Version A — {result['version_a']['overall_score']}/10")
                st.write(result["version_a"]["summary"])
                for s in result["version_a"].get("suggestions", []):
                    st.markdown(f"→ {s}")
            with col2:
                st.subheader(f"Version B — {result['version_b']['overall_score']}/10")
                st.write(result["version_b"]["summary"])
                for s in result["version_b"].get("suggestions", []):
                    st.markdown(f"→ {s}")
