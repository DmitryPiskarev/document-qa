from openai import OpenAI, OpenAIError
from pdf_parser import parse_pdf
from docx_parser import parse_docx


def analyze_resume(uploaded_file, job_description, api_key=None, use_mock=True):
    """
    Analyze resume vs job description.
    Returns tuple: (resume_text, {"score": int/str, "suggestions": list[str], "improved_cv": str})
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

    # 2️⃣ Mock output
    if use_mock or not api_key:
        improved_cv = f"""
        # John Doe
        📧 john.doe@email.com | 📱 +123456789 | 🌐 linkedin.com/in/johndoe  

        ## Experience
        - Led a team of 5 engineers to deliver project X  
        - Improved system efficiency by 25%  

        ## Education
        - B.Sc. Computer Science, XYZ University
        """
        return resume_text, {
            "score": 85,
            "suggestions": [
                "Rewrite bullet 1 to highlight leadership",
                "Add keyword 'Python' in experience section",
                "Emphasize results using numbers"
            ],
            "improved_cv": improved_cv
        }

    # 3️⃣ Call OpenAI API
    client = OpenAI(api_key=api_key)
    prompt = f"""
    Here is a resume:
    {resume_text}

    Here is a job description:
    {job_description}

    Tasks:
    1. Give a match score from 0 to 100.
    2. Suggest rewritten bullets / improvements.
    3. Rewrite the resume in a modern, minimalistic style (like a NYT newsletter).
       Preserve contact details and structure (Contact, Experience, Education).
       Return in Markdown format.
    """

    messages = [{"role": "user", "content": prompt}]

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
        )

        content = response.choices[0].message.content
        # Naive parsing: split sections
        if "## Suggestions" in content:
            parts = content.split("##")
            suggestions = parts[1].strip().splitlines()
            improved_cv = "##".join(parts[2:]) if len(parts) > 2 else ""
        else:
            suggestions = content.splitlines()
            improved_cv = ""

        return resume_text, {
            "score": "See GPT output",
            "suggestions": [s.strip("-• ") for s in suggestions if s.strip()],
            "improved_cv": improved_cv
        }

    except OpenAIError as e:
        return resume_text, {"score": "Error", "suggestions": [str(e)], "improved_cv": ""}
