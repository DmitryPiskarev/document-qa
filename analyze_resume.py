# analyze_resume.py
from openai import OpenAI
from pdf_parser import parse_pdf


def analyze_resume(uploaded_file, job_description, api_key):
    # 1️⃣ Read document
    if uploaded_file.name.endswith(".pdf"):
        resume_text = parse_pdf(uploaded_file)
    else:
        resume_text = uploaded_file.read().decode()

    # 2️⃣ GPT prompt
    prompt_score = f"""
    Here is a resume:
    {resume_text}

    Here is a job description:
    {job_description}

    1. Give a match score from 0 to 100 on how well this resume matches the job.
    2. Suggest rewritten bullets / improvements to better match the job description.
    """
    messages = [{"role": "user", "content": prompt_score}]

    # OpenAI client
    # client = OpenAI(api_key=api_key)
    # stream = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=messages,
    #     stream=True,
    # )
    #
    # # Collect response
    # response_text = ""
    # for event in stream:
    #     if event.type == "response.output_text.delta":
    #         response_text += event.delta

    return {
        "score": 85,
        "suggestions": [
            "Rewrite bullet 1",
            "Add keyword 'Python'",
            "Highlight leadership experience"
        ]
    }
    # return {"score": "See GPT output", "suggestions": response_text.split("\n")}
