import streamlit as st
from analyze_resume import analyze_resume
from utils import normalize_cv_markdown, extract_keywords
from components.copy_button import st_copy_to_clipboard
from export import export_docx, export_pdf

st.set_page_config(page_title="CV Matcher", page_icon="📄", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .card {
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0.6rem;
            background-color: #f9f9f9;
            border: 1px solid #e6e6e6;
            box-shadow: 1px 2px 6px rgba(0,0,0,0.05);
        }
        .metric-card {
            text-align: center;
            font-size: 1.8rem;
            font-weight: bold;
            color: #2c3e50;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #7f8c8d;
        }
        .section-title {
            font-weight: 600;
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            color: #34495e;
        }
        /* Copy button styling */
        .st-copy-to-clipboard-btn {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-weight: 500 !important;
            padding: 6px 14px !important;
            border-radius: 6px !important;
            min-height: 38px !important;
            margin-left: auto !important;
            line-height: 1.6 !important;
            color: white !important;
            background-color: #2c7be5 !important;
            border: none !important;
            cursor: pointer !important;
        }
        .st-copy-to-clipboard-btn:hover {
            background-color: #1a5bb8 !important;
            color: white !important;
        }
        .st-copy-to-clipboard-btn:active {
            background-color: #155a9c !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("📄 CV ↔ Job Description Matcher")
st.caption("Get a match score, improvement suggestions, and a polished resume rewrite.")

# --- API Key ---
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")

else:
    # Check if we already have results
    has_result = "analysis_result" in st.session_state

    if has_result:
        col_left, col_right = st.columns([1, 2])
    else:
        # Before analysis → center everything
        col_left = st.container()
        col_right = None

    with col_left:
        # --- Sidebar (left column) ---
        with st.sidebar:
            st.title("📄 CV Matcher Settings")
            openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")

            uploaded_file = st.file_uploader("📎 Upload your Resume", type=("txt", "md", "pdf", "docx"))
            job_description = st.text_area(
                "💼 Paste Job Description",
                placeholder="Paste the job description here...",
                disabled=not uploaded_file,
            )

            if uploaded_file and job_description and openai_api_key:
                if st.button("🚀 Analyze Resume", use_container_width=True):
                    with st.spinner("Analyzing resume, please wait..."):
                        resume_text, result = analyze_resume(
                            uploaded_file, job_description, openai_api_key, use_mock=False
                        )
                    st.session_state["resume_text"] = resume_text
                    st.session_state["analysis_result"] = result
                    st.rerun()
    # --- Results area (right column) ---
    if has_result and col_right:
        result = st.session_state["analysis_result"]
        resume_text = st.session_state["resume_text"]

        with col_right:
            st.success("✅ Analysis complete!")

            # --- Score and Recommendations ---
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(
                    f"""
                    <div class='card metric-card'>
                        {result['score']}
                        <div class='metric-label'>Match Score</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("✨ Suggestions for Improvement")
                if "recommendations" in result:
                    for section, bullets in result["recommendations"].items():
                        st.markdown(f"<div class='section-title'>{section}</div>", unsafe_allow_html=True)
                        for bullet in bullets:
                            st.markdown(f"- {bullet}")
                else:
                    for bullet in result.get("suggestions", []):
                        st.markdown(f"- {bullet}")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Keyword Coverage ---
            job_keywords = extract_keywords(job_description, top_n=20)
            resume_text_lower = resume_text.lower()
            keyword_status = {kw: ("✅" if kw in resume_text_lower else "❌") for kw in job_keywords}

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("🔑 Keyword Coverage")
            for kw, status in keyword_status.items():
                color = "green" if status == "✅" else "red"
                st.markdown(f"- <span style='color:{color}'>{status} {kw}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # --- Improved Resume ---
            if result.get("improved_cv"):
                clean_cv = normalize_cv_markdown(result["improved_cv"])
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                col_title, col_button = st.columns([5, 1])
                with col_title:
                    st.subheader("📝 Improved Resume (Preview)")
                with col_button:
                    st_copy_to_clipboard(
                        text=clean_cv,
                        before_copy_label="📋 Copy Resume",
                        after_copy_label="✅ Copied!",
                        key="resume_copy"
                    )

                st.markdown(result["improved_cv"], unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # --- Download Buttons ---
                st.download_button(
                    label="📥 Download as DOCX",
                    data=export_docx(clean_cv),
                    file_name="improved_resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

                st.download_button(
                    label="📥 Download as PDF",
                    data=export_pdf(clean_cv),
                    file_name="improved_resume.pdf",
                    mime="application/pdf"
                )

            with st.expander("📄 Original Resume (parsed text)"):
                st.text_area("Resume text", resume_text, height=300)
