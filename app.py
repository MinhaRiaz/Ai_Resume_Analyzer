import io
import json
import os
from typing import Any

import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader
from docx import Document


MODEL_NAME = "gemini-3.8-flash"
MAX_FILE_SIZE_MB = 10

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "ats_score": {
            "type": "integer",
            "description": "Overall ATS-readiness score from 0 to 100."
        },
        "score_label": {
            "type": "string",
            "description": "One of: Excellent, Good, Fair, or Needs Improvement."
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
                    "explanation": {"type": "string"}
                },
                "required": ["category", "score", "max_score", "explanation"]
            }
        },
        "strengths": {
            "type": "array",
            "items": {"type": "string"}
        },
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
                    "example": {"type": "string"}
                },
                "required": [
                    "priority", "area", "issue", "recommendation", "example"
                ]
            }
        },
        "missing_keywords": {
            "type": "array",
            "items": {"type": "string"}
        },
        "detected_sections": {
            "type": "array",
            "items": {"type": "string"}
        },
        "keyword_matches": {
            "type": "array",
            "items": {"type": "string"}
        },
        "summary": {
            "type": "string",
            "description": "A concise recruiter-style assessment."
        }
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
        "summary"
    ]
}


def get_api_key() -> str:
    """Read the Gemini key from Streamlit secrets first, then environment."""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""

    return key or os.getenv("GEMINI_API_KEY", "")


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


def extract_resume_text(uploaded_file) -> tuple[str, bool]:
    """Return text and whether the file should be sent as a native PDF."""
    data = uploaded_file.getvalue()
    suffix = uploaded_file.name.lower().rsplit(".", 1)[-1]

    if suffix == "pdf":
        # We still extract text locally for validation/fallback, but Gemini
        # receives the original PDF so it can reason about document structure.
        return extract_text_from_pdf(data), True

    if suffix == "docx":
        return extract_text_from_docx(data), False

    if suffix == "txt":
        return data.decode("utf-8", errors="replace").strip(), False

    raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT.")


def build_prompt(resume_text: str, job_description: str) -> str:
    job_context = (
        job_description.strip()
        if job_description.strip()
        else "No specific job description was provided. Evaluate against "
             "general ATS-friendly resume standards."
    )

    return f"""
You are an expert ATS resume evaluator and technical recruiter.

Analyze the resume below. The purpose is to estimate how well the resume
will perform in common Applicant Tracking Systems and recruiter screening.

IMPORTANT:
- Do not claim that this is the exact score of any particular ATS vendor.
- This is an ATS-readiness estimate based on a transparent 100-point rubric.
- Be evidence-based. Do not invent experience, skills, employers, degrees,
  certifications, dates, or achievements that are not present.
- Recommendations must be realistic and actionable.
- If a job description is supplied, prioritize relevant keywords and skills
  from it. Do not recommend keyword stuffing.
- A keyword should be considered a match only when the resume actually
  contains the term or a clear equivalent.
- Consider formatting risks such as tables, columns, graphics, icons,
  headers/footers, unusual section names, and overly complex layouts when
  the document gives you enough evidence. Do not assume a formatting issue
  without evidence.
- For bullet improvements, preserve the user's facts and only improve
  wording/structure. If you cannot safely create an example, use an
  instruction such as "Add a quantified result if you can verify it."

SCORING RUBRIC (must total 100):
1. ATS formatting and parseability: 20
2. Contact/header information: 10
3. Standard sections and organization: 15
4. Job-description keyword alignment: 20
5. Experience bullet quality and impact: 15
6. Skills section quality: 10
7. Education/certifications: 5
8. Overall ATS/recruiter readiness: 5

If there is no job description, score keyword alignment using broadly useful
keywords appropriate to the candidate's apparent field, but clearly state
that the score is less targeted.

JOB DESCRIPTION:
{job_context}

RESUME TEXT:
{resume_text[:50000]}
""".strip()


def analyze_resume(
    file_bytes: bytes,
    filename: str,
    extracted_text: str,
    job_description: str,
    api_key: str,
) -> dict[str, Any]:
    client = genai.Client(api_key=api_key)

    suffix = filename.lower().rsplit(".", 1)[-1]
    prompt = build_prompt(extracted_text, job_description)

    if suffix == "pdf":
        contents = [
            types.Part.from_bytes(
                data=file_bytes,
                mime_type="application/pdf",
            ),
            prompt,
        ]
    else:
        contents = [prompt]

    if suffix != "pdf":
        contents = [
            prompt,
            "\nFULL EXTRACTED RESUME:\n" + extracted_text[:50000],
        ]

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RESPONSE_SCHEMA,
            temperature=0.2,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    try:
        result = json.loads(response.text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini returned invalid JSON.") from exc

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
        raise RuntimeError(f"Gemini response is missing fields: {sorted(missing)}")

    result["ats_score"] = max(0, min(100, int(result["ats_score"])))

    breakdown = result["score_breakdown"]
    if len(breakdown) != 8:
        raise RuntimeError("Unexpected score breakdown returned by Gemini.")

    total = sum(int(item["score"]) for item in breakdown)
    max_total = sum(int(item["max_score"]) for item in breakdown)

    if max_total != 100 or total != result["ats_score"]:
        # Normalize only when the model's category total is inconsistent.
        # This keeps the displayed overall score internally consistent.
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
        page_title="Resume ATS Analyzer",
        page_icon="📄",
        layout="wide",
    )

    st.title("📄 Resume ATS Analyzer")
    st.caption(
        "Upload your resume to get an AI-powered ATS-readiness score, "
        "keyword analysis, and actionable improvements."
    )

    with st.sidebar:
        st.header("Settings")
        st.info(
            "Gemini 2.5 Flash is used for the resume analysis. "
            "The score is an ATS-readiness estimate, not a score from a "
            "specific ATS vendor."
        )
        st.markdown("**Supported:** PDF, DOCX, TXT")
        st.markdown("**Recommended:** Add the target job description for a "
                    "more meaningful keyword score.")

    api_key = get_api_key()
    if not api_key:
        st.error(
            "Gemini API key not found. Add GEMINI_API_KEY to Streamlit "
            "Secrets or your environment variables."
        )
        st.stop()

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "txt"],
        help="Maximum recommended file size is 10 MB.",
    )

    job_description = st.text_area(
        "Target job description (optional, but recommended)",
        height=220,
        placeholder=(
            "Paste the job description here. The analyzer will compare "
            "your resume against it and identify missing/relevant keywords."
        ),
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
            "2. Optionally paste the target job description.\n"
            "3. Gemini 2.5 Flash evaluates ATS readiness.\n"
            "4. Review your score, matched/missing keywords, strengths, "
            "and prioritized improvements."
        )
        return

    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error(f"Please upload a file smaller than {MAX_FILE_SIZE_MB} MB.")
        return

    if not analyze_button:
        st.success(f"Ready to analyze **{uploaded_file.name}**.")
        return

    try:
        file_bytes = uploaded_file.getvalue()
        extracted_text, is_pdf = extract_resume_text(uploaded_file)

        if not extracted_text.strip():
            if is_pdf:
                st.warning(
                    "No selectable text was extracted from this PDF. "
                    "Gemini will still inspect the PDF, but a scanned/image-only "
                    "resume may reduce text-based ATS analysis accuracy."
                )
            else:
                st.error("No readable text was found in the uploaded file.")
                return

        with st.spinner("Analyzing your resume with Gemini 2.5 Flash..."):
            result = analyze_resume(
                file_bytes=file_bytes,
                filename=uploaded_file.name,
                extracted_text=extracted_text,
                job_description=job_description,
                api_key=api_key,
            )

        st.session_state["analysis"] = result

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
        for item in result["score_breakdown"]:
            score = int(item["score"])
            maximum = int(item["max_score"])
            st.write(f"**{item['category']} — {score}/{maximum}**")
            st.progress(min(score / maximum, 1.0) if maximum else 0.0)
            st.caption(item["explanation"])

    with col2:
        st.subheader("🧾 Recruiter Summary")
        st.write(result["summary"])

        st.subheader("💪 Strengths")
        for strength in result["strengths"]:
            st.markdown(f"- {strength}")

        st.subheader("📌 Detected Sections")
        st.write(", ".join(result["detected_sections"]) or "None detected")

    st.markdown("---")

    key_col1, key_col2 = st.columns(2)

    with key_col1:
        st.subheader("✅ Keyword Matches")
        if result["keyword_matches"]:
            for keyword in result["keyword_matches"]:
                st.markdown(f"- `{keyword}`")
        else:
            st.info("No strong keyword matches were identified.")

    with key_col2:
        st.subheader("⚠️ Missing / Suggested Keywords")
        if result["missing_keywords"]:
            for keyword in result["missing_keywords"]:
                st.markdown(f"- `{keyword}`")
        else:
            st.success("No major missing keywords were identified.")

    st.markdown("---")
    st.subheader("🛠️ Prioritized Improvements")

    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    improvements = sorted(
        result["improvements"],
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

    st.markdown("---")
    st.caption(
        "Privacy note: resumes may contain personal information. Do not "
        "upload documents you are not authorized to share. Files are sent "
        "to Google's Gemini API for analysis."
    )


if __name__ == "__main__":
    main()
