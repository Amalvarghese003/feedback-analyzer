import streamlit as st
import pandas as pd
from textblob import TextBlob
import os

# Load existing teacher/subject/department data
if os.path.exists("teachers.csv"):
    teacher_df = pd.read_csv("teachers.csv")
else:
    teacher_df = pd.DataFrame(columns=["Teacher Name", "Subject", "Department"])

# Load or create results.csv
if os.path.exists("results.csv"):
    results_df = pd.read_csv("results.csv")

else:
    results_df = pd.DataFrame(columns=[
        "Name", "Year", "Branch", "Department",
        "Teacher Name", "Subject", "Feedback", "Sentiment"
    ])

st.title("🎓 Smart Feedback Sentiment Analyzer")

# Student Form
st.subheader("📝 Student Feedback Form")

reg_number = st.text_input("Enter your Register Number")
name = st.text_input("Enter your Name")
year = st.selectbox("Select Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
branch = st.selectbox("Select Branch", ["AI & ML", "CSE", "ECE", "EEE", "ME", "CE"])

# Dropdowns from teacher data
if not teacher_df.empty:
    department = st.selectbox("Select Department", teacher_df["Department"].unique())
    filtered_teachers = teacher_df[teacher_df["Department"] == department]
    teacher_name = st.selectbox("Select Teacher", filtered_teachers["Teacher Name"].unique())
    subject = st.selectbox("Select Subject", filtered_teachers["Subject"].unique())
else:
    st.warning("Admin has not added teacher/subject data yet.")
    department = teacher_name = subject = ""

feedback = st.text_area("Enter your feedback")

if st.button("Submit Feedback"):
    if name and feedback and teacher_name:
        sentiment_score = TextBlob(feedback).sentiment.polarity
        sentiment = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"

        new_row = pd.DataFrame([{
            "Name": name, "Year": year, "Branch": branch,
            "Department": department, "Teacher Name": teacher_name,
            "Subject": subject, "Feedback": feedback, "Sentiment": sentiment
        }])
        results_df = pd.concat([results_df, new_row], ignore_index=True)
        results_df.to_csv("results.csv", index=False)
        st.success("✅ Feedback submitted and sentiment analyzed!")
    else:
        st.warning("❗Please fill all fields properly.")

# 📊 View all feedback (Admin Only)
st.markdown( "---" )
st.subheader( "🔐 Admin Access Only" )

admin_password = st.text_input( "Enter admin password to view all feedback", type="password" )

if admin_password == "admin123":
    st.success( "Access granted. Welcome admin!" )

    # Check if results.csv exists and is not empty
    if not results_df.empty:
        st.subheader( "📄 View All Feedback" )
        st.dataframe( results_df )
    else:
        st.info( "No feedback submitted yet." )
else:
    st.info( "Only admins can view the feedback data." )
