# 📄 Resume ATS Analyzer

An AI-powered **Resume ATS Analyzer** built with **Streamlit** and **Google Gemini 3.6 Flash**.

The application analyzes a resume and provides an estimated **ATS-readiness score out of 100**, detailed scoring breakdown, keyword matching, missing keywords, strengths, detected resume sections, and prioritized recommendations for improvement.

> **Note:** The score is an ATS-readiness estimate and is not an official score from any specific Applicant Tracking System (ATS) vendor.

---

## 🚀 Features

### 🎯 ATS Readiness Score

Get an overall resume score from **0–100** based on multiple ATS and recruiter-focused factors.

### 📊 8-Category Score Breakdown

The analyzer evaluates the resume using a transparent 100-point rubric:

| Category                           | Maximum Score |
| ---------------------------------- | ------------: |
| ATS Formatting & Parseability      |            20 |
| Contact/Header Information         |            10 |
| Standard Sections & Organization   |            15 |
| Job Description Keyword Alignment  |            20 |
| Experience Bullet Quality & Impact |            15 |
| Skills Section Quality             |            10 |
| Education/Certifications           |             5 |
| Overall ATS/Recruiter Readiness    |             5 |
| **Total**                          |       **100** |

### 🔑 Keyword Analysis

When a target job description is provided, the application identifies:

* Matching keywords
* Potentially missing keywords
* Relevant technical skills
* Job-specific terminology
* Areas where the resume could better align with the position

The application avoids recommending keyword stuffing.

### 💪 Resume Strengths

The AI identifies the strongest aspects of the resume, such as:

* Relevant technical skills
* Strong experience
* Effective project descriptions
* Good resume structure
* Relevant keywords
* Quantified achievements

### 🛠️ Prioritized Improvements

The application provides actionable recommendations organized by priority:

* High
* Medium
* Low

Each recommendation includes:

* Area
* Issue
* Recommendation
* Example

### 📋 Detected Resume Sections

The analyzer detects sections such as:

* Contact Information
* Summary
* Skills
* Experience
* Education
* Projects
* Certifications
* Achievements

### 📄 Multiple File Formats

Supported resume formats:

* PDF
* DOCX
* TXT

PDF files are also sent to Gemini in their original format, allowing Gemini to inspect the document itself in addition to locally extracted text.

### 🔐 API Key Security

The Gemini API key is **not hardcoded** into the application.

The application reads the key from:

```text
GEMINI_API_KEY
```

using Streamlit Secrets or an environment variable.

---

# 🧠 How It Works

The application follows this workflow:

```text
                 ┌─────────────────┐
                 │  Upload Resume  │
                 └────────┬────────┘
                          │
                          ▼
              ┌──────────────────────┐
              │ Extract Resume Text  │
              │ PDF / DOCX / TXT     │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Optional Job         │
              │ Description          │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Build AI Evaluation  │
              │ Prompt + ATS Rubric  │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Gemini 2.5 Flash     │
              │ Analysis             │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Structured JSON      │
              │ Response             │
              └──────────┬───────────┘
                         │
                         ▼
       ┌─────────────────────────────────────┐
       │          ATS Analysis Results       │
       ├─────────────────────────────────────┤
       │ Overall Score                       │
       │ Score Breakdown                     │
       │ Recruiter Summary                   │
       │ Strengths                            │
       │ Keyword Matches                     │
       │ Missing Keywords                    │
       │ Detected Sections                   │
       │ Prioritized Improvements             │
       └─────────────────────────────────────┘
```

---

# 🛠️ Tech Stack

* **Python**
* **Streamlit** — Web application interface
* **Google Gemini 2.5 Flash** — AI-powered resume analysis
* **Google GenAI SDK** — Gemini API integration
* **PyPDF** — PDF text extraction
* **python-docx** — DOCX text extraction
* **JSON Schema** — Structured AI responses

---

# 📁 Project Structure

```text
ai-resume-analyzer/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-resume-analyzer.git
```

Go into the project directory:

```bash
cd ai-resume-analyzer
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Gemini API Key Setup

You need a Google Gemini API key to run the application.

Create your API key through Google's Gemini API/AI Studio service.

Do **not** put the API key directly inside `app.py`.

## Option 1 — Streamlit Secrets

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Your project should look like:

```text
ai-resume-analyzer/
│
├── app.py
├── requirements.txt
├── README.md
│
└── .streamlit/
    └── secrets.toml
```

### ⚠️ Important

Never upload `secrets.toml` to GitHub.

Add this to `.gitignore`:

```text
.streamlit/secrets.toml
```

---

# ▶️ Run Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📤 Using the Application

### Step 1 — Upload Resume

Upload a resume in one of the supported formats:

```text
PDF
DOCX
TXT
```

### Step 2 — Add Job Description

Paste the target job description into the job description field.

This is optional, but strongly recommended because it makes keyword analysis more relevant to the specific position.

### Step 3 — Analyze

Click:

```text
🔍 Analyze Resume
```

### Step 4 — Review Results

The application provides:

* ATS readiness score
* Score breakdown
* Recruiter summary
* Strengths
* Keyword matches
* Missing keywords
* Detected sections
* Prioritized improvements

---

# 📊 Scoring System

The application uses a transparent 100-point scoring model.

### 1. ATS Formatting & Parseability — 20 points

Evaluates potential issues involving:

* Complex layouts
* Columns
* Tables
* Graphics
* Icons
* Headers and footers
* Text extraction
* ATS readability

### 2. Contact/Header Information — 10 points

Evaluates whether important contact information is clearly presented.

### 3. Standard Sections & Organization — 15 points

Evaluates the presence and organization of standard resume sections.

### 4. Job Description Keyword Alignment — 20 points

Compares the resume against the supplied job description.

### 5. Experience Bullet Quality & Impact — 15 points

Evaluates:

* Action verbs
* Results
* Achievements
* Quantification
* Clarity
* Impact

### 6. Skills Section Quality — 10 points

Evaluates the relevance, organization, and clarity of listed skills.

### 7. Education/Certifications — 5 points

Evaluates the presentation and relevance of education and certifications.

### 8. Overall ATS/Recruiter Readiness — 5 points

Provides an overall assessment from an ATS and recruiter perspective.

---

# 🧪 Example Result

A resume might receive:

```text
ATS Readiness Score
78/100

Good
```

With results such as:

```text
ATS Formatting & Parseability       17/20
Contact/Header Information           9/10
Standard Sections & Organization    12/15
Keyword Alignment                  15/20
Experience Bullet Quality           10/15
Skills Section Quality               7/10
Education/Certifications             4/5
Overall Readiness                    4/5
────────────────────────────────────────
Total                               78/100
```

---

# 🔒 Privacy

Resumes can contain sensitive personal and professional information.

Users should only upload documents they are authorized to share.

When an analysis is performed, the application sends resume information to the **Google Gemini API** for AI analysis.

Do not upload confidential documents unless you understand and accept the applicable data-handling policies.

---

# ⚠️ Limitations

This application provides an **estimated ATS-readiness score**.

It does not reproduce the scoring algorithm of any particular ATS vendor.

Results may vary depending on:

* Resume format
* Job description
* Industry
* Job role
* Keywords
* Resume content
* AI interpretation

The application should be used as a resume optimization aid rather than a guarantee of passing an ATS.

---

# 🚀 Deployment on Streamlit Community Cloud

You can deploy the application for free using Streamlit Community Cloud.

## 1. Push the project to GitHub

Your repository should contain:

```text
app.py
requirements.txt
README.md
.gitignore
```

Do **not** upload:

```text
.streamlit/secrets.toml
```

or your API key.

## 2. Connect GitHub to Streamlit

Create a new application on Streamlit Community Cloud and select your GitHub repository.

Set the main file to:

```text
app.py
```

## 3. Add the API Secret

In your Streamlit application's settings, open **Secrets** and add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Save the secret and restart/redeploy the application.

---

# 🔮 Future Improvements

Possible future features include:

* Resume rewriting
* Job-specific resume optimization
* Cover letter generation
* Resume keyword highlighting
* Resume comparison
* Multiple resume versions
* Downloadable ATS reports
* PDF report generation
* LinkedIn profile optimization
* Job-role-specific scoring
* Resume version history
* More AI model providers

---

# 🤝 Contributing

Contributions are welcome.

To contribute:

```bash
git clone https://github.com/YOUR-USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer
```

Create a new branch:

```bash
git checkout -b feature/new-feature
```

Make your changes and commit:

```bash
git add .
git commit -m "Add new feature"
```

Push the branch:

```bash
git push origin feature/new-feature
```

Then create a Pull Request on GitHub.

---

# 📜 License

This project is intended for educational and portfolio purposes.

Add an appropriate open-source license if you plan to distribute the project publicly.

---

# 👩‍💻 Author

**Minha Khan**

Built with:

* Python
* Streamlit
* Google Gemini
* AI-powered resume analysis

---

## ⭐ If You Find This Project Useful

Consider giving the repository a ⭐ on GitHub and sharing it with others who are preparing their resumes for ATS-based recruitment.

```
```
