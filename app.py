import streamlit as st
import pandas as pd
from textblob import TextBlob
import os

# Load teachers.csv
if os.path.exists("teachers.csv"):
    teacher_df = pd.read_csv("teachers.csv")
else:
    teacher_df = pd.DataFrame(columns=["Teacher Name", "Subject", "Department"])

# Load or create results.csv
RESULTS_FILE = "results.csv"
RESULTS_COLS = [
    "Feedback_ID", "Register_Number", "Name", "Year", "Branch",
    "Department", "Teacher_Name", "Subject", "Feedback_Text", "Sentiment"
]

if os.path.exists(RESULTS_FILE):
    results_df = pd.read_csv(RESULTS_FILE)
else:
    results_df = pd.DataFrame(columns=RESULTS_COLS)

# Student Feedback Form UI
st.title("🎓 Student Feedback Form (v2)")

reg_no = st.text_input("Enter your Register Number")
name = st.text_input("Enter your Name")
year = st.selectbox("Select Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
branch = st.selectbox("Select Branch", ["AI & ML", "CSE", "ECE", "EEE", "ME", "CE"])

if not teacher_df.empty:
    department = st.selectbox("Select Department", teacher_df["Department"].unique())
    filtered = teacher_df[teacher_df["Department"] == department]
    teacher_name = st.selectbox("Select Teacher", filtered["Teacher Name"].unique())
    subject = st.selectbox("Select Subject", filtered["Subject"].unique())
else:
    department = teacher_name = subject = ""
    st.warning("⚠️ No teacher data available. Contact Admin.")

feedback = st.text_area("Enter your feedback")

# Submit button
if st.button("Submit Feedback"):
    if reg_no and name and feedback and teacher_name:
        sentiment = TextBlob(feedback).sentiment.polarity
        sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"

        new_row = {
            "Feedback_ID": len(results_df) + 1,
            "Register_Number": reg_no,
            "Name": name,
            "Year": year,
            "Branch": branch,
            "Department": department,
            "Teacher_Name": teacher_name,
            "Subject": subject,
            "Feedback_Text": feedback,
            "Sentiment": sentiment_label
        }

        results_df = pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)
        results_df.to_csv(RESULTS_FILE, index=False)
        st.success("✅ Feedback submitted successfully!")
    else:
        st.warning("Please fill all fields before submitting.")
