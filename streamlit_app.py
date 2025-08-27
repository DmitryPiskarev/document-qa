import streamlit as st
from openai import OpenAI
from analyze_resume import analyze_resume

st.set_page_config(page_title="CV Matcher", page_icon="📄", layout="wide")

# Title
st.title("📄 CV ↔ Job Description Matcher")
st.caption("Get a match score, improvement suggestions, and a polished resume rewrite.")

# API Key
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
        if st.button("🚀 Analyze Resume"):
            with st.spinner("Analyzing resume, please wait..."):
                resume_text, result = analyze_resume(uploaded_file, job_description, openai_api_key, use_mock=False)

            st.success("✅ Analysis complete!")

            # Layout in 2 columns
            col1, col2 = st.columns([1, 2])

            with col1:
                st.metric(label="Match Score", value=result["score"])

            with col2:
                st.subheader("✨ Suggestions for Improvement")
                for bullet in result["suggestions"]:
                    st.markdown(f"✔️ {bullet}")

            # Improved Resume
            if result["improved_cv"]:
                st.subheader("📝 Improved Resume (Preview)")
                st.markdown(result["improved_cv"])

                st.download_button(
                    "📥 Download Improved Resume (Markdown)",
                    data=result["improved_cv"],
                    file_name="improved_resume.md",
                    mime="text/markdown",
                )

            # Original Resume
            with st.expander("📄 Original Resume (parsed text)"):
                st.text_area("Resume text", resume_text, height=300)
