# 💼 JobMatch

JobMatch is an interactive resume analysis tool that compares a candidate's resume with a job description and generates an overall job-fit score, skill analysis, and actionable insights.

## 🚀 Features

- 📄 Extracts text from uploaded PDF resumes
- 🔍 Calculates semantic similarity between resume and job description
- 🧠 Extracts relevant skills from both documents
- ⚖️ Uses weighted skill matching to prioritize required skills
- 🎯 Classifies skills as required or preferred
- 📊 Generates an overall match score
- 🔎 Identifies matched and missing skills
- 💡 Provides actionable insights to improve resume-job alignment
- 🌐 Interactive web interface built with Streamlit

## 🛠️ Tech Stack

- Python
- Streamlit
- Scikit-learn
- Sentence Transformers
- PyMuPDF

## 📈 How It Works

```text
Resume PDF
    ↓
Text Extraction
    ↓
Skill Extraction ──────────┐
                           ↓
Job Description → Skill Classification
                           ↓
             Semantic + Skill Matching
                           ↓
                  Overall Match Score
                           ↓
             Skill Gap + Insights