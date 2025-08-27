import streamlit as st
from openai import OpenAI
from analyze_resume import analyze_resume

# Show title and description.
st.title("📄 Match your CV with Job Description!")
st.write(
    "Upload your Resume + Job description below and see how much they fit each other. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload your Resume (.txt or .md for now)", type=("txt", "md")
    )

    job_description = st.text_area(
        "Paste Job Description",
        placeholder="Paste the job description here...",
        disabled=not uploaded_file,
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and job_description:
        if st.button("Analyze Resume"):
            # Call analysis function here
            result = analyze_resume(uploaded_file, job_description)
            st.write("Match Score:", result["score"])
            st.write("Suggestions:")
            for bullet in result["suggestions"]:
                st.write("-", bullet)

    # if uploaded_file and question:
    #
    #     # Process the uploaded file and question.
    #     document = uploaded_file.read().decode()
    #     messages = [
    #         {
    #             "role": "user",
    #             "content": f"Here's a document: {document} \n\n---\n\n {question}",
    #         }
    #     ]
    #
    #     # Generate an answer using the OpenAI API.
    #     stream = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=messages,
    #         stream=True,
    #     )
    #
    #     # Stream the response to the app using `st.write_stream`.
    #     st.write_stream(stream)
