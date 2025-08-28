import streamlit as st
from analyze_resume import analyze_resume
from utils import normalize_cv_markdown
from st_copy_to_clipboard import st_copy_to_clipboard

st.set_page_config(page_title="CV Matcher", page_icon="📄", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
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
        .copy-btn {
            background-color: #2c7be5;
            color: white;
            border: none;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .copy-btn:hover {
            background-color: #1a5bb8;
        }
        
        /* Target the copy button */
        button[data-baseweb="button"] {
            background-color: #2c7be5 !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 8px 14px !important;
            font-size: 14px !important;
            border: none !important;
            transition: background 0.2s;
        }

        button[data-baseweb="button"]:hover {
            background-color: #1a5bb8 !important;
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
            margin-left: auto !important;  /* push to right */
            line-height: 1.6 !important;
            color: white !important;
            background-color: #2c7be5 !important;
            border: none !important;
            cursor: pointer !important;
        }

        .st-copy-to-clipboard-btn:hover {
            background-color: #1a5bb8 !important;
            color: white !important;
            border-color: #1a5bb8 !important;
        }

        .st-copy-to-clipboard-btn:active {
            background-color: #155a9c !important;
            color: white !important;
        }

        /* Optional: align button right next to section header */
        .improved-resume-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
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
    uploaded_file = st.file_uploader("📎 Upload your Resume", type=("txt", "md", "pdf", "docx"))
    job_description = st.text_area(
        "💼 Paste Job Description",
        placeholder="Paste the job description here...",
        disabled=not uploaded_file,
    )

    if uploaded_file and job_description:
        if st.button("🚀 Analyze Resume", use_container_width=True):
            with st.spinner("Analyzing resume, please wait..."):
                resume_text, result = analyze_resume(
                    uploaded_file, job_description, openai_api_key, use_mock=True
                )

            # --- Persist results ---
            st.session_state["resume_text"] = resume_text
            st.session_state["analysis_result"] = result

    # --- Display results if available ---
    if "analysis_result" in st.session_state:
        result = st.session_state["analysis_result"]
        resume_text = st.session_state["resume_text"]

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

        # --- Improved Resume ---
        if result.get("improved_cv"):
            clean_cv = normalize_cv_markdown(result["improved_cv"])
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            col_title, col_button = st.columns([5, 1])

            st.markdown(f"""
            <div class="card">
                <div class="improved-resume-header">
                    <h4>📝 Improved Resume (Preview)</h4>
                    {st_copy_to_clipboard(clean_cv, return_html=True)}
                </div>
                <div>{result["improved_cv"]}</div>
            </div>
            """, unsafe_allow_html=True)

            with col_title:
                st.subheader("📝 Improved Resume (Preview)")

            with col_button:
                # Copy button, styled, minimalistic
                st_copy_to_clipboard(clean_cv)

            st.markdown(result["improved_cv"], unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # --- Original Resume ---
        with st.expander("📄 Original Resume (parsed text)"):
            st.text_area("Resume text", resume_text, height=300)
