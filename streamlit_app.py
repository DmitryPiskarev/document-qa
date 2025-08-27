import streamlit as st
from openai import OpenAI
from analyze_resume import analyze_resume

# Show title and description.
st.title("📄 Match your CV with Job Description!")
st.write("Upload your Resume + Job description below and see how much they fit each other.")

openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    uploaded_file = st.file_uploader(
        "📎 Upload your Resume (.txt, .md, or .pdf)",
        type=("txt", "md", "pdf")
    )

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

            # Match Score
            st.metric(label="Match Score", value=result["score"])

            # Suggestions
            st.subheader("✨ Suggestions for Improvement")
            for bullet in result["suggestions"]:
                st.markdown(f"- ✅ **{bullet}**")

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

            # Original
            with st.expander("📄 Original Resume (parsed text)"):
                st.text_area("Resume text", resume_text, height=300)
