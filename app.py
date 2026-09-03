import streamlit as st

from pdf_parser import extract_text_from_pdf
from matcher import (
    calculate_similarity,
    extract_skills,
    calculate_overall_match,
    classify_job_skills,
    calculate_weighted_skill_match,
    get_skill_breakdown,
)

def generate_insight(
    overall_match,
    similarity,
    missing_required,
    missing_preferred,
):
    if missing_required:
        skills = ", ".join(
            skill.title() for skill in sorted(missing_required)
        )
        return (
            "⚠️ **Important skill gap:** The resume does not currently "
            f"show these required skills: {skills}. If you have genuine "
            "experience with them, make that experience more visible."
        )

    if overall_match >= 0.70:
        if missing_preferred:
            skills = ", ".join(
                skill.title() for skill in sorted(missing_preferred)
            )
            return (
                "🟢 **Strong match:** You meet all detected required skills. "
                f"To improve further, consider highlighting relevant experience "
                f"with: {skills}."
            )

        return (
            "🟢 **Excellent match:** The resume covers all detected required "
            "and preferred skills and has strong overall alignment."
        )

    if similarity < 0.60:
        return (
            "🟡 **Skills are covered, but experience alignment is lower.** "
            "Consider making projects and experience bullets more specific to "
            "the responsibilities in this role."
        )

    return (
        "🟡 **Good foundation:** The resume covers the detected required skills, "
        "but adding more role-specific achievements could strengthen the match."
    )


def format_skill_list(skills):
    """Return a readable skill list for the results screen."""
    return ", ".join(skill.title() for skill in sorted(skills))


def render_skill_gap_analysis(
    matched_required,
    missing_required,
    matched_preferred,
    missing_preferred,
):
    """Show an at-a-glance view of the candidate's detected skill coverage."""
    required_total = len(matched_required) + len(missing_required)
    preferred_total = len(matched_preferred) + len(missing_preferred)

    st.subheader("🎯 Skill Gap Analysis")

    required_col, preferred_col = st.columns(2)

    with required_col:
        if required_total:
            st.metric(
                "Required skills covered",
                f"{len(matched_required)}/{required_total}",
                f"{len(missing_required)} missing",
                delta_color="inverse",
            )
        else:
            st.metric("Required skills covered", "No skills detected")

    with preferred_col:
        if preferred_total:
            st.metric(
                "Preferred skills covered",
                f"{len(matched_preferred)}/{preferred_total}",
                f"{len(missing_preferred)} missing",
                delta_color="inverse",
            )
        else:
            st.metric("Preferred skills covered", "No skills detected")

    if required_total:
        if missing_required:
            st.warning(
                "**Missing required skills:** "
                f"{format_skill_list(missing_required)}"
            )
        else:
            st.success("All detected required skills are covered.")

        if matched_required:
            st.write(
                "**Matched required skills:** "
                f"{format_skill_list(matched_required)}"
            )

    if preferred_total:
        if missing_preferred:
            st.info(
                "**Missing preferred skills:** "
                f"{format_skill_list(missing_preferred)}"
            )

        if matched_preferred:
            st.write(
                "**Matched preferred skills:** "
                f"{format_skill_list(matched_preferred)}"
            )

    if not required_total and not preferred_total:
        st.info(
            "No recognised skills were found in the job description. "
            "Try including a requirements or preferred-skills section."
        )

st.set_page_config(
    page_title="JobMatch",
    page_icon="💼",
    layout="wide",
)

st.title("💼 JobMatch")
st.write("Analyze how well your resume matches a job description.")

resume_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
)

job_description = st.text_area(
    "Paste the job description",
    height=250,
    placeholder="Paste the job description here...",
)

if st.button("Analyze Match"):
    if resume_file is None:
        st.warning("Please upload a resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        with open("uploaded_resume.pdf", "wb") as file:
            file.write(resume_file.getbuffer())

        resume_text = extract_text_from_pdf("uploaded_resume.pdf")

        similarity = calculate_similarity(
            resume_text,
            job_description,
        )

        resume_skills = extract_skills(resume_text)

        required_skills, preferred_skills = classify_job_skills(
            job_description
        )

        weighted_skill_match = calculate_weighted_skill_match(
            resume_skills,
            required_skills,
            preferred_skills,
        )

        (
            matched_required,
            missing_required,
            matched_preferred,
            missing_preferred,
        ) = get_skill_breakdown(
            resume_skills,
            required_skills,
            preferred_skills,
        )

        overall_match = calculate_overall_match(
            similarity,
            weighted_skill_match,
        )

        st.divider()
        st.header("📊 Match Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Overall Match",
                f"{overall_match:.0%}",
            )

        with col2:
            st.metric(
                "Semantic Similarity",
                f"{similarity:.0%}",
            )

        with col3:
            st.metric(
                "Weighted Skill Match",
                f"{weighted_skill_match:.0%}",
            )

        render_skill_gap_analysis(
            matched_required,
            missing_required,
            matched_preferred,
            missing_preferred,
        )

        st.subheader("📋 Required Skills")

        for skill in sorted(matched_required):
            st.write(f"✓ {skill.title()}")

        for skill in sorted(missing_required):
            st.write(f"✗ {skill.title()}")

        st.subheader("⭐ Preferred Skills")

        for skill in sorted(matched_preferred):
            st.write(f"✓ {skill.title()}")

        for skill in sorted(missing_preferred):
            st.write(f"• {skill.title()}")

        st.subheader("💡 Key Insight")

        insight = generate_insight(
            overall_match,
            similarity,
            missing_required,
            missing_preferred,
        )

        st.info(insight)


        
