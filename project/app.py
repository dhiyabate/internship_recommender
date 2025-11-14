import os
import pandas as pd
import streamlit as st

# =========================
# Load CSV files
# =========================
BASE_DIR = os.path.dirname(__file__)
students = pd.read_csv(os.path.join(BASE_DIR, "students.csv"))
internships = pd.read_csv(os.path.join(BASE_DIR, "internships.csv"))

# =========================
# Streamlit App Layout
# =========================
st.title("Internship Recommendation System 🏢")

# Select a student
student_name = st.selectbox("Select a student:", students["Name"])

# If a student is selected
if student_name:
    student = students[students["Name"] == student_name].iloc[0]
    st.subheader(f"Student Profile: {student_name}")
    st.write(f"- GPA: {student['GPA']}")
    st.write(f"- Skills: {student['Skills']}")
    st.write(f"- Preferred Domain: {student['PreferredDomain']}")
    st.write(f"- Location Preference: {student['LocationPref']}")

    # =========================
    # Fuzzy Logic Scoring
    # =========================
    def score_internship(student, internship):
        score = 0

        # 1️⃣ GPA weight
        if student['GPA'] >= 3.5:
            score += 10
        elif student['GPA'] >= 3.0:
            score += 6
        else:
            score += 3

        # 2️⃣ Skill match weight
        student_skills = [s.strip().lower() for s in student['Skills'].split(",")]
        if internship['SkillRequired'].strip().lower() in student_skills:
            score += 10

        # 3️⃣ Domain match weight
        if student['PreferredDomain'].strip().lower() == internship['Domain'].strip().lower():
            score += 5

        # 4️⃣ Location match weight
        if student['LocationPref'].strip().lower() == internship['Location'].strip().lower():
            score += 3

        return score

    # Compute scores
    internships['Score'] = internships.apply(lambda x: score_internship(student, x), axis=1)

    # Sort and get top 3
    top_internships = internships.sort_values(by='Score', ascending=False).head(3)

    # =========================
    # Display Recommendations
    # =========================
    st.subheader("Top 3 Internship Recommendations ✨")
    st.table(top_internships[['InternshipID','Company','Domain','Location','SkillRequired','Score']])
