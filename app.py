import io
import json
import os
from typing import Any

import streamlit as st
from docx import Document
from groq import Groq, GroqError
from pypdf import PdfReader

# Groq models suitable for structured JSON extraction
MODEL_NAME = "openai/gpt-oss-120b"
MAX_FILE_SIZE_MB = 10

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "ats_score": {
            "type": "integer",
            "description": "Overall ATS-readiness score from 0 to 100.",
        },
        "score_label": {
            "type": "string",
            "description": "One of: Excellent, Good, Fair, or Needs Improvement.",
        },
        "score_breakdown": {
            "type": "array",
            "description": "Exactly 8 scoring categories. The points must add to 100.",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "score": {"type": "integer"},
                    "max_score": {"type": "integer"},
                    "explanation": {"type": "string"},
                },
                "required": ["category", "score", "max_score", "explanation"],
            },
        },
        "strengths": {"type": "array", "items": {"type": "string"}},
        "improvements": {
            "type": "array",
            "description": "Specific, actionable resume improvements.",
            "items": {
                "type": "object",
                "properties": {
                    "priority": {"type": "string"},
                    "area": {"type": "string"},
                    "issue": {"type": "string"},
                    "recommendation": {"type": "string"},
                    "example": {"type": "string"},
                },
                "required": [
                    "priority",
                    "area",
                    "issue",
                    "recommendation",
                    "example",
                ],
            },
        },
        "missing_keywords": {"type": "array", "items": {"type": "string"}},
        "detected_sections": {"type": "array", "items": {"type": "string"}},
        "keyword_matches": {"type": "array", "items": {"type": "string"}},
        "summary": {
            "type": "string",
            "description": "A concise recruiter-style assessment.",
        },
    },
    "required": [
        "ats_score",
        "score_label",
        "score_breakdown",
        "strengths",
        "improvements",
        "missing_keywords",
        "detected_sections",
        "keyword_matches",
        "summary",
    ],
}


def get_api_key() -> str:
    """Read the Groq API key from Streamlit secrets or environment variables."""
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        key = ""

    return key or os.getenv("GROQ_API_KEY", "")


def extract_text_from_docx(data: bytes) -> str:
    document = Document(io.BytesIO(data))
    chunks = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            chunks.append(text)

    for table in document.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            row_text = " | ".join(cell for cell in cells if cell)
            if row_text:
                chunks.append(row_text)

    return "\n".join(chunks)


def extract_text_from_pdf(data: bytes) -> str:
    reader = PdfReader(io.BytesIO(data))
    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text)

    return "\n".join(pages).strip()


def extract_resume_text(uploaded_file) -> str:
    """Extract text from the uploaded PDF, DOCX, or TXT file."""
    data = uploaded_file.getvalue()
    suffix = uploaded_file.name.lower().rsplit(".", 1)[-1]

    if suffix == "pdf":
        return extract_text_from_pdf(data)
    if suffix == "docx":
        return extract_text_from_docx(data)
    if suffix == "txt":
        return data.decode("utf-8", errors="replace").strip()

    raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT.")


def build_prompt(resume_text: str, job_description: str) -> str:
    job_context = (
        job_description.strip()
        if job_description.strip()
        else "No specific job description was provided. Evaluate against general ATS-friendly resume standards."
    )

    return f"""
You are an expert ATS resume evaluator and technical recruiter.

Analyze the resume text provided. Your task is to evaluate how well it will perform in Applicant Tracking Systems and recruiter screening.

IMPORTANT RULES:
- Return ONLY valid JSON matching the exact schema requested.
- Do not claim this is the exact score of any specific ATS vendor.
- This is an ATS-readiness estimate based on a transparent 100-point rubric.
- Be evidence-based. Do not invent experience or skills not present in the text.
- If a job description is supplied, prioritize relevant keywords and skills from it.

SCORING RUBRIC (must total 100 across the 8 categories):
1. ATS formatting and parseability: 20
2. Contact/header information: 10
3. Standard sections and organization: 15
4. Job-description keyword alignment: 20
5. Experience bullet quality and impact: 15
6. Skills section quality: 10
7. Education/certifications: 5
8. Overall ATS/recruiter readiness: 5

JOB DESCRIPTION:
{job_context}

RESUME TEXT:
{resume_text[:30000]}
""".strip()


def analyze_resume(
    extracted_text: str,
    job_description: str,
    api_key: str,
) -> dict[str, Any]:
    client = Groq(api_key=api_key)
    prompt = build_prompt(extracted_text, job_description)

    # Groq Chat Completion with JSON mode enforced
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": f"You are an ATS Resume Analyzer. Respond strictly in valid JSON matching this schema:\n{json.dumps(RESPONSE_SCHEMA)}",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    response_content = response.choices[0].message.content
    if not response_content:
        raise RuntimeError("Groq API returned an empty response.")

    try:
        result = json.loads(response_content)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Groq returned invalid JSON format.") from exc

    validate_result(result)
    return result


def validate_result(result: dict[str, Any]) -> None:
    required = {
        "ats_score",
        "score_label",
        "score_breakdown",
        "strengths",
        "improvements",
        "missing_keywords",
        "detected_sections",
        "keyword_matches",
        "summary",
    }

    missing = required - set(result)
    if missing:
        raise RuntimeError(f"Response is missing fields: {sorted(missing)}")

    result["ats_score"] = max(0, min(100, int(result["ats_score"])))

    breakdown = result.get("score_breakdown", [])
    if len(breakdown) != 8:
        st.warning("Score breakdown category count differed slightly from expected 8.")

    total = sum(int(item.get("score", 0)) for item in breakdown)
    if total != result["ats_score"]:
        result["ats_score"] = max(0, min(100, total))


def score_class(score: int) -> str:
    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Good"
    if score >= 50:
        return "Fair"
    return "Needs Improvement"


def render_score(score: int) -> None:
    st.metric("ATS Readiness Score", f"{score}/100", score_class(score))
    st.progress(score / 100)


def main() -> None:
    st.set_page_config(
        page_title="Resume ATS Analyzer (Groq)",
        page_icon="📄",
        layout="wide",
    )

    st.title("📄 Resume ATS Analyzer")
    st.caption("Powered by Groq LPUs for ultra-fast analysis")

    with st.sidebar:
        st.markdown("**Supported:** PDF, DOCX, TXT")
        st.markdown(
            "**Recommended:** Add target job description for keyword scoring."
        )

    api_key = get_api_key()
    if not api_key:
        st.error(
            "Groq API key not found. Please set `GROQ_API_KEY` in `.streamlit/secrets.toml` or environment variables."
        )
        st.stop()

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "txt"],
        help="Maximum recommended file size is 10 MB.",
    )

    job_description = st.text_area(
        "Target job description (optional)",
        height=200,
        placeholder="Paste job description here...",
    )

    analyze_button = st.button(
        "🔍 Analyze Resume",
        type="primary",
        use_container_width=True,
    )

    if not uploaded_file:
        st.markdown("---")
        st.subheader("How it works")
        st.markdown(
            "1. Upload your resume.\n"
            "2. Optionally paste target job description.\n"
            "3. Groq evaluates ATS readiness instantly.\n"
            "4. Review keyword matches, missing terms, and suggestions."
        )
        return

    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error(f"Please upload a file smaller than {MAX_FILE_SIZE_MB} MB.")
        return

    if not analyze_button:
        st.success(f"Ready to analyze **{uploaded_file.name}**.")
        return

    try:
        extracted_text = extract_resume_text(uploaded_file)

        if not extracted_text.strip():
            st.error(
                "No readable text found. Scanned PDFs without OCR are not supported."
            )
            return

        with st.spinner("Analyzing your resume with Groq..."):
            result = analyze_resume(
                extracted_text=extracted_text,
                job_description=job_description,
                api_key=api_key,
            )

        st.session_state["analysis"] = result

    except GroqError as e:
        st.error(f"Groq API Error: {e.message if hasattr(e, 'message') else e}")
        return
    except Exception as exc:
        st.error("Analysis failed.")
        st.exception(exc)
        return

    result = st.session_state.get("analysis")
    if not result:
        return

    st.markdown("---")
    render_score(int(result["ats_score"]))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Score Breakdown")
        for item in result.get("score_breakdown", []):
            score = int(item["score"])
            maximum = int(item["max_score"])
            st.write(f"**{item['category']} — {score}/{maximum}**")
            st.progress(min(score / maximum, 1.0) if maximum else 0.0)
            st.caption(item["explanation"])

    with col2:
        st.subheader("🧾 Recruiter Summary")
        st.write(result.get("summary", ""))

        st.subheader("💪 Strengths")
        for strength in result.get("strengths", []):
            st.markdown(f"- {strength}")

        st.subheader("📌 Detected Sections")
        st.write(
            ", ".join(result.get("detected_sections", [])) or "None detected"
        )

    st.markdown("---")

    key_col1, key_col2 = st.columns(2)

    with key_col1:
        st.subheader("✅ Keyword Matches")
        if result.get("keyword_matches"):
            for keyword in result["keyword_matches"]:
                st.markdown(f"- `{keyword}`")
        else:
            st.info("No strong keyword matches identified.")

    with key_col2:
        st.subheader("⚠️ Missing / Suggested Keywords")
        if result.get("missing_keywords"):
            for keyword in result["missing_keywords"]:
                st.markdown(f"- `{keyword}`")
        else:
            st.success("No major missing keywords identified.")

    st.markdown("---")
    st.subheader("🛠️ Prioritized Improvements")

    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    improvements = sorted(
        result.get("improvements", []),
        key=lambda x: priority_order.get(str(x.get("priority")), 3),
    )

    for index, item in enumerate(improvements, start=1):
        priority = item.get("priority", "Medium")
        with st.expander(
            f"{index}. {item.get('area', 'Improvement')} — {priority}"
        ):
            st.write(f"**Issue:** {item.get('issue', '')}")
            st.write(f"**Recommendation:** {item.get('recommendation', '')}")
            if item.get("example"):
                st.markdown("**Example:**")
                st.info(item["example"])


if __name__ == "__main__":
    main()
