from openai import OpenAI, OpenAIError
from pdf_parser import parse_pdf
from docx_parser import parse_docx
import json


def analyze_resume(uploaded_file, job_description, api_key=None, use_mock=True):
    """
    Analyze resume vs job description.
    Returns tuple: (resume_text, {"score": int, "suggestions": list[str], "improved_cv": str})
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
        return resume_text, {"score": "Error parsing file", "suggestions": [str(e)], "improved_cv": ""}

    # 2️⃣ Mock output (for dev/demo without API calls)
    if use_mock or not api_key:
        return resume_text, {
            "score": 85,
            "suggestions": [
                "Highlight PyTorch and CatBoost",
                "Explicitly mention LLMs in customer support automation",
                "Add measurable business outcomes to bullets"
            ],
            "improved_cv": """# John Doe
📧 john.doe@email.com | 📱 +123456789 | 🌐 linkedin.com/in/johndoe  

## Experience
- Led a team of 5 engineers, delivering project X with 20% faster cycle time  
- Built NLP pipeline with transformers improving classification accuracy by 18%  

## Education
- B.Sc. Computer Science — XYZ University  
"""
        }

    # 3️⃣ Call OpenAI API
    client = OpenAI(api_key=api_key)
    prompt = f"""
    You are a professional career consultant. Analyze the following resume against the job description.
    Your goal is to provide a **structured improvement plan** and then rewrite the resume so it matches the role better.
    
    Respond ONLY with valid JSON in this schema:
    
    {{
      "score": <integer 0-100>,
      "skills_score": <integer 0-100>,
      "education_score": <integer 0-100>,
      "experience_score": <integer 0-100>,
      "keyword_score": <integer 0-100>,
      "formatting_score": <integer 0-100>,
      "recommendations": {{
          "Skills & Keywords": ["bullet 1", "bullet 2", "bullet 3"],
          "Experience Relevance": ["bullet 1", "bullet 2"],
          "Impact & Metrics": ["bullet 1", "bullet 2"],
          "Formatting & Clarity": ["bullet 1"]
      }},
      "improved_cv": "<resume rewritten in clean Markdown with clear sections>"
    }}
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        content = response.choices[0].message.content

        # Parse JSON safely
        data = json.loads(content)
        return resume_text, data

    except (OpenAIError, json.JSONDecodeError) as e:
        return resume_text, {"score": "Error", "suggestions": [str(e)], "improved_cv": ""}
