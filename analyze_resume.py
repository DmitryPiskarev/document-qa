
def analyze_resume(uploaded_file, job_description):
    # 1️⃣ Read document
    resume_text = uploaded_file.read().decode()

    # 2️⃣ Compute similarity / match score (optional embedding)
    # For MVP, we can just rely on GPT to judge match:
    prompt_score = f"""
    Here is a resume:
    {resume_text}

    Here is a job description:
    {job_description}

    1. Give a match score from 0 to 100 on how well this resume matches the job.
    2. Suggest rewritten bullets / improvements to better match the job description.
    """
    messages = [{"role": "user", "content": prompt_score}]

    # Call OpenAI API (same as template)
    client = OpenAI(api_key=openai_api_key)
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )

    # Collect response as text
    response_text = ""
    for event in stream:
        if event.type == "response.output_text.delta":
            response_text += event.delta

    # Parse response: you could split score vs suggestions, or just show full text
    return {"score": "See GPT output", "suggestions": response_text.split("\n")}
