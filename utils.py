import re


def normalize_cv_markdown(md_text: str) -> str:
    """
    Normalize CV markdown for consistent PDF generation.
    Returns clean markdown with:
    - Name as '# Name'
    - Contacts in one line
    - Sections as '## Section'
    - Roles/Companies as '### Role/Company'
    - Lists standardized with '-'
    """
    lines = md_text.splitlines()
    normalized = []
    contacts_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            normalized.append("")
            continue

        # Normalize headers
        if re.match(r"^#{1,6}\s", line):
            content = re.sub(r"^#{1,6}\s+", "", line)
            if "Name" in content or "PhD" in content or re.match(r"^[A-Z][a-z]+\s[A-Z][a-z]+", content):
                normalized.append(f"# {content}")  # Name
            else:
                normalized.append(f"## {content}")  # Section
            continue

        # Merge bold role/company lines to ### format
        if line.startswith("**") and line.endswith("**"):
            content = line.strip("* ")
            normalized.append(f"### {content}")
            continue

        # Contact info
        if line.startswith(("📧", "📞", "🌐")):
            contacts_lines.append(line)
            continue

        # Normalize lists
        if line.startswith(("-", "*")):
            content = line.lstrip("-* ").strip()
            normalized.append(f"- {content}")
            continue

        # Default: just clean text
        normalized.append(line)

    # Combine contacts into single line after name
    if contacts_lines:
        normalized.insert(1, " | ".join(contacts_lines))
        normalized.insert(2, "")  # blank line after contacts

    return "\n".join(normalized)
