# analyze_resume.py
from openai import OpenAI, OpenAIError
from pdf_parser import parse_pdf
from docx_parser import parse_docx


def analyze_resume(uploaded_file, job_description, api_key=None, use_mock=True):
    """
    Analyze resume vs job description.
    Returns dict: {"score": int/str, "suggestions": list of str}
    """

    # 1️⃣ Parse uploaded file
    filename = uploaded_file.name.lower()
    try:
        if filename.endswith(".pdf"):
            resume_text = parse_pdf(uploaded_file)
        elif filename.endswith(".docx"):
            resume_text = parse_docx(uploaded_file)
        else:  # txt, md, etc.
            resume_text = uploaded_file.read().decode()
    except Exception as e:
        return {"score": "Error parsing file", "suggestions": [str(e)]}

    # 2️⃣ Mock output (useful for testing UI without API quota)
    if use_mock or not api_key:
        return resume_text, {
            "score": 85,
            "suggestions": [
                "Rewrite bullet 1 to highlight leadership",
                "Add keyword 'Python' in experience section",
                "Emphasize results using numbers"
            ]
        }

    # 3️⃣ Call OpenAI API
    client = OpenAI(api_key=api_key)
    prompt_score = f"""
    Here is a resume:
    {resume_text}

    Here is a job description:
    {job_description}

    1. Give a match score from 0 to 100 on how well this resume matches the job.
    2. Suggest rewritten bullets / improvements to better match the job description.
    """

    messages = [{"role": "user", "content": prompt_score}]

    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        response_text = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta:
                response_text += chunk.choices[0].delta.get("content", "")

        suggestions = [line for line in response_text.split("\n") if line.strip()]
        return resume_text, {"score": "See GPT output", "suggestions": suggestions}

    except OpenAIError as e:
        return resume_text, {"score": "Error", "suggestions": [str(e)]}

