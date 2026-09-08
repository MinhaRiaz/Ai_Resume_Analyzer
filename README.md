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

              │ Gemini 3.6 Flash     │

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

* **Google Gemini 3.6 Flash** — AI-powered resume analysis

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



### `app.py`



Contains the Streamlit user interface, resume processing, Gemini API integration, scoring logic, and result display.



### `requirements.txt`



Contains all Python packages required to run the application.



### `README.md`



Contains project documentation, setup instructions, usage instructions, and deployment information.



### `.gitignore`



Prevents sensitive files, API keys, virtual environments, and unnecessary Python files from being uploaded to GitHub.



---



# ⚙️ Installation



Follow these steps to run the application on your computer.



## 1. Clone the Repository



Open Command Prompt or PowerShell and run:



```bash

git clone https://github.com/YOUR-USERNAME/ai-resume-analyzer.git

```



Move into the project directory:



```bash

cd ai-resume-analyzer

```



---



## 2. Create a Virtual Environment



### Windows



```bash

python -m venv venv

```



Activate the virtual environment:



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



## 3. Install Dependencies



Install all required packages using:



```bash

pip install -r requirements.txt

```



---



# 🔑 Gemini API Key Setup



The application requires a Google Gemini API key.



The API key should **never be written directly inside `app.py`** or committed to GitHub.



## Option 1 — Streamlit Secrets



For local development, create the following folder inside the project:



```text

.streamlit/

```



Inside it, create:



```text

secrets.toml

```



Your project should look like:



```text

ai-resume-analyzer/

│

├── app.py

├── requirements.txt

├── README.md

├── .gitignore

│

└── .streamlit/

    └── secrets.toml

```



Add your API key to `secrets.toml`:



```toml

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

```



### ⚠️ Important



Never upload:



```text

.streamlit/secrets.toml

```



to GitHub.



Make sure your `.gitignore` contains:



```text

.streamlit/secrets.toml

```



You can also ignore:



```text

venv/

__pycache__/

*.pyc

.env

```



---



# ▶️ Run the Application Locally



After installing the dependencies and configuring your API key, start the Streamlit application:



```bash

streamlit run app.py

```



Streamlit will start the application locally.



You can normally access it at:



```text

http://localhost:8501

```



The application can also open automatically in your default web browser.



---



# 📤 How to Use the Application



## Step 1 — Upload Your Resume



Upload your resume in one of the supported formats:



```text

PDF

DOCX

TXT

```



---



## Step 2 — Add a Job Description



Paste the target job description into the job description field.



This step is optional, but it is **strongly recommended** because it allows the analyzer to perform more relevant keyword and job-alignment analysis.



---



## Step 3 — Analyze Your Resume



Click:



```text

🔍 Analyze Resume

```



The application sends the required resume information and evaluation prompt to Gemini for analysis.



---



## Step 4 — Review Your Results



The application provides:



* 🎯 ATS readiness score

* 📊 Score breakdown

* 📝 Recruiter summary

* 💪 Resume strengths

* 🔑 Matching keywords

* ⚠️ Missing keywords

* 📋 Detected resume sections

* 🛠️ Prioritized improvements



---



# 📊 Scoring System



The application uses a transparent **100-point scoring model**.



## 1. ATS Formatting & Parseability — 20 Points



Evaluates potential issues involving:



* Complex layouts

* Columns

* Tables

* Graphics

* Icons

* Headers and footers

* Text extraction

* ATS readability



---



## 2. Contact/Header Information — 10 Points



Evaluates whether important contact information is clearly presented and easy to identify.



---



## 3. Standard Sections & Organization — 15 Points



Evaluates the presence, naming, organization, and structure of standard resume sections.



---



## 4. Job Description Keyword Alignment — 20 Points



Compares the resume against the supplied job description and evaluates relevant terminology and skills.



---



## 5. Experience Bullet Quality & Impact — 15 Points



Evaluates:



* Action verbs

* Results

* Achievements

* Quantification

* Clarity

* Impact



---



## 6. Skills Section Quality — 10 Points



Evaluates the relevance, organization, and clarity of the listed skills.



---



## 7. Education/Certifications — 5 Points



Evaluates the presentation and relevance of education and certifications.



---



## 8. Overall ATS/Recruiter Readiness — 5 Points



Provides an overall assessment from both an ATS and recruiter perspective.



---



# 🧪 Example Result



A resume might receive:



```text

ATS Readiness Score



78/100



Good

```



Example breakdown:



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



The application also provides qualitative feedback explaining why the resume received its score and how it can be improved.



---



# 🌐 Live Application



You can use the deployed application directly without installing Python or configuring an API key locally.



### 🚀 Try the Application



👉 **[Open Resume ATS Analyzer](YOUR_STREAMLIT_APP_URL)**



> Replace `YOUR_STREAMLIT_APP_URL` with your actual Streamlit deployment URL.



---



# 🔒 Privacy



Resumes may contain sensitive personal and professional information.



Users should only upload documents they are authorized to share.



During analysis, relevant resume information may be sent to the **Google Gemini API** for AI processing.



Do not upload confidential documents unless you understand and accept the applicable data-handling and privacy policies.



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



The application should be used as a **resume optimization and analysis aid**, not as a guarantee of passing an ATS.



---



# ☁️ Deployment on Streamlit Community Cloud



The application can be deployed using **Streamlit Community Cloud**.



## 1. Push the Project to GitHub



Your GitHub repository should contain:



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



or your Gemini API key.



---



## 2. Connect GitHub to Streamlit



Open Streamlit Community Cloud and sign in with your GitHub account.



Create a new application and select:



* GitHub repository

* Branch

* Main file



Set the main file to:



```text

app.py

```



Then deploy the application.



---



## 3. Add the Gemini API Secret



After deployment, open your application's settings and locate **Secrets**.



Add:



```toml

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

```



Save the secret and restart/redeploy the application.



The deployed application will then be able to access the Gemini API without exposing the API key in your GitHub repository.



---



## 4. Add Your Live App URL to README



After successful deployment, Streamlit will provide a URL similar to:



```text

https://your-app-name.streamlit.app

```



Copy that URL and replace:



```text

YOUR_STREAMLIT_APP_URL

```



in this README.



For example:



```markdown

👉 **[Open Resume ATS Analyzer](https://your-app-name.streamlit.app)**

```



This creates a clickable link on your GitHub README.



---



# 🔮 Future Improvements



Possible future features include:



* ✍️ AI-powered resume rewriting

* 🎯 Job-specific resume optimization

* 📝 Cover letter generation

* 🔑 Resume keyword highlighting

* 📊 Resume comparison

* 📄 Multiple resume versions

* 📥 Downloadable ATS reports

* 📑 PDF report generation

* 💼 LinkedIn profile optimization

* 🎯 Job-role-specific scoring

* 🕐 Resume version history

* 🤖 Support for additional AI model providers



---



# 🤝 Contributing



Contributions are welcome.



To contribute to the project:



### 1. Clone the repository



```bash

git clone https://github.com/YOUR-USERNAME/ai-resume-analyzer.git

```



### 2. Enter the project directory



```bash

cd ai-resume-analyzer

```



### 3. Create a new branch



```bash

git checkout -b feature/new-feature

```



### 4. Make your changes



Implement and test your changes locally.



### 5. Commit your changes



```bash

git add .

git commit -m "Add new feature"

```



### 6. Push your branch



```bash

git push origin feature/new-feature

```



Then create a Pull Request on GitHub.



---



# 📜 License



This project is intended for educational and portfolio purposes.



If you plan to distribute this project publicly, consider adding an appropriate open-source license such as the MIT License.



---



# 👩‍💻 Author



**Minha Khan**



Computer Science Student | AI & Software Development



### Built With



* 🐍 Python

* 🎈 Streamlit

* ✨ Google Gemini 3.6 Flash

* 📄 PyPDF

* 📝 python-docx



---



# ⭐ Support



If you find this project useful, consider giving the repository a ⭐ on GitHub.



Your feedback and suggestions are also welcome!
