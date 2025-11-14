import streamlit as st
import pandas as pd

# Load data
students = pd.read_csv("students.csv")
internships = pd.read_csv("internships.csv")

st.title("Internship Recommendation System")

st.subheader("Select a student")
student_name = st.selectbox("Student:", students["Name"])

if student_name:
    student = students[students["Name"] == student_name].iloc[0]
    st.write("GPA:", student["GPA"])
    st.write("Skills:", student["Skills"])
    
    # Simple recommendation logic
    recommended = internships[internships["SkillRequired"].str.contains(student["Skills"].split(",")[0])]
    
    st.subheader("Recommended Internships")
    st.table(recommended)
