# 📄 Resume ATS Analyzer

An AI-powered **Resume ATS Analyzer** built with **Streamlit** and **Groq API (openai/gpt-oss-120b)**.

> 🚀 **[Try the Live App](https://ai-resume-analyzer-app-1.streamlit.app/)**

The application analyzes a resume and provides an estimated **ATS-readiness score out of 100**, detailed scoring breakdown, keyword matching, missing keywords, strengths, detected resume sections, and prioritized recommendations for improvement.

> **Note:** The score is an ATS-readiness estimate and is not an official score from any specific Applicant Tracking System (ATS) vendor.

---

## 🚀 Features

### 🎯 ATS Readiness Score

Get an overall resume score from **0–100** based on multiple ATS and recruiter-focused factors.

### 📊 8-Category Score Breakdown

The analyzer evaluates the resume using a transparent 100-point rubric:

| Category                            | Maximum Score |
| ---------------------------------- | ------------: |
| ATS Formatting & Parseability      |            20 |
| Contact/Header Information         |            10 |
| Standard Sections & Organization   |            15 |
| Job Description Keyword Alignment  |            20 |
| Experience Bullet Quality & Impact |            15 |
| Skills Section Quality             |            10 |
| Education/Certifications            |             5 |
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

* 🔴 High
* 🟡 Medium
* 🟢 Low

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

Text extracted locally is sent securely to Groq LPUs for lightning-fast analysis.

### 🔐 API Key Security

The Groq API key is **not hardcoded** into the application.

The application reads:

```text
GROQ_API_KEY
