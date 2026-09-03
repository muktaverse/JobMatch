import logging
import re

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(resume_text, job_description):
    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_description])

    similarity = cosine_similarity(resume_embedding, job_embedding)

    return similarity[0][0]

SKILLS = {
    # Programming
    "python": ["python", "python3"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "c": ["c programming", "c language"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],

    # Web Development
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "react.js", "reactjs"],
    "node.js": ["node.js", "nodejs", "node"],
    "rest apis": ["rest api", "rest apis", "restful api", "restful apis"],
    "git": ["git", "version control"],

    # Databases
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres", "postgres sql"],
    "mongodb": ["mongodb", "mongo db"],

    # Data / ML / AI
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "natural language processing": [
        "natural language processing",
        "nlp"
    ],
    "data analysis": ["data analysis", "data analytics"],
    "data science": ["data science"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn"],

    # Computer Science
    "data structures": [
        "data structures",
        "data structure"
    ],
    "algorithms": [
        "algorithms",
        "algorithm"
    ],
    "data structures and algorithms": [
        "data structures and algorithms",
        "dsa"
    ],
    "object-oriented programming": [
        "object-oriented programming",
        "object oriented programming",
        "oop"
    ],

    # Cloud / DevOps
    "aws": ["aws", "amazon web services"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],

    # UX / Design
    "figma": ["figma"],
    "sketch": ["sketch"],
    "invision": ["invision"],
    "wireframing": [
        "wireframe",
        "wireframes",
        "wireframing"
    ],
    "prototyping": [
        "prototype",
        "prototypes",
        "prototyping"
    ],
    "user research": [
        "user research",
        "user requirements"
    ],
    "product design": [
        "product design",
        "product designer"
    ],
    "ux design": [
        "ux design",
        "ux designer",
        "user experience design"
    ],
    "ui design": [
        "ui design",
        "ui designer",
        "user interface design"
    ],
    "android": ["android"],
    "ios": ["ios"],
}

def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill, variations in SKILLS.items():
        for variation in variations:
            pattern = r"\b" + re.escape(variation) + r"\b"

            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return found_skills

def calculate_skill_match(resume_skills, job_skills):
    if not job_skills:
        return 0

    matched_skills = set(resume_skills) & set(job_skills)

    score = len(matched_skills) / len(set(job_skills))

    return score

def calculate_overall_match(semantic_similarity, skill_match):
    overall_score = (
        semantic_similarity * 0.60
        + skill_match * 0.40
    )

    return overall_score

def classify_job_skills(job_description):
    text = job_description.lower()

    required_skills = []
    preferred_skills = []

    required_keywords = [
        "required skills",
        "required",
        "requirements",
        "must have",
        "must-have"
    ]

    preferred_keywords = [
        "preferred skills",
        "preferred",
        "nice to have",
        "nice-to-have",
        "bonus",
        "plus"
    ]

    # Find where the required and preferred sections start
    required_position = -1
    preferred_position = -1

    for keyword in required_keywords:
        position = text.find(keyword)

        if position != -1:
            required_position = position
            break

    for keyword in preferred_keywords:
        position = text.find(keyword)

        if position != -1:
            preferred_position = position
            break

    # Extract skills from the appropriate sections
    if required_position != -1:

        if preferred_position != -1 and preferred_position > required_position:
            required_section = text[
                required_position:preferred_position
            ]
        else:
            required_section = text[required_position:]

        required_skills = extract_skills(required_section)

    if preferred_position != -1:
        preferred_section = text[preferred_position:]

        preferred_skills = extract_skills(preferred_section)

    return required_skills, preferred_skills

def calculate_weighted_skill_match(
    resume_skills,
    required_skills,
    preferred_skills
):
    required_skills = set(required_skills)
    preferred_skills = set(preferred_skills)
    resume_skills = set(resume_skills)

    required_match = (
        len(resume_skills & required_skills)
        / len(required_skills)
        if required_skills
        else 0
    )

    preferred_match = (
        len(resume_skills & preferred_skills)
        / len(preferred_skills)
        if preferred_skills
        else 0
    )

    weighted_score = (
        required_match * 0.70
        + preferred_match * 0.30
    )

    return weighted_score

def get_skill_breakdown(resume_skills, required_skills, preferred_skills):
    resume_skills = set(resume_skills)
    required_skills = set(required_skills)
    preferred_skills = set(preferred_skills)

    matched_required = resume_skills & required_skills
    missing_required = required_skills - resume_skills

    matched_preferred = resume_skills & preferred_skills
    missing_preferred = preferred_skills - resume_skills

    return (
        matched_required,
        missing_required,
        matched_preferred,
        missing_preferred
    )

