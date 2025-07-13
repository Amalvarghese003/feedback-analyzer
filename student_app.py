import streamlit as st
import pandas as pd
from textblob import TextBlob
import os

# ---------- Load teacher / subject / department data ----------
if os.path.exists("teachers.csv"):
    teacher_df = pd.read_csv("teachers.csv")
else:
    teacher_df = pd.DataFrame(columns=["Teacher Name", "Subject", "Department"])

# ---------- Load or create results.csv ----------
RESULTS_FILE = "results.csv"
RESULTS_COLS = [
    "Feedback_ID", "Register_Number", "Name", "Year", "Branch",
    "Department", "Teacher_Name", "Subject", "Feedback_Text", "Sentiment"
]

if os.path.exists(RESULTS_FILE):
    results_df = pd.read_csv(RESULTS_FILE)
else:
    results_df = pd.DataFrame(columns=RESULTS_COLS)

st.title("📋 Student Feedback Form")

# ----- Form inputs -----
reg_no = st.text_input("Register Number")
name   = st.text_input("Name")
year   = st.selectbox("Year", ["1st", "2nd", "3rd", "4th"])
branch = st.selectbox("Branch", ["AI & ML", "CSE", "ECE", "EEE", "ME", "CE"])

if not teacher_df.empty:
    department   = st.selectbox("Department", teacher_df["Department"].unique())
    filtered     = teacher_df[teacher_df["Department"] == department]
    teacher_name = st.selectbox("Teacher",  filtered["Teacher Name"].unique())
    subject      = st.selectbox("Subject",  filtered["Subject"].unique())
else:
    st.warning("Admin has not added teachers yet.")
    department = teacher_name = subject = ""

feedback_text = st.text_area("Your feedback")

# ----- Submit button -----
if st.button("Submit Feedback"):
    if reg_no and name and feedback_text and teacher_name:
        polarity  = TextBlob(feedback_text).sentiment.polarity
        sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
        feedback_id = len(results_df) + 1

        row = {
            "Feedback_ID": feedback_id,
            "Register_Number": reg_no,
            "Name": name,
            "Year": year,
            "Branch": branch,
            "Department": department,
            "Teacher_Name": teacher_name,
            "Subject": subject,
            "Feedback_Text": feedback_text,
            "Sentiment": sentiment
        }

        results_df = pd.concat([results_df, pd.DataFrame([row])], ignore_index=True)
        results_df.to_csv(RESULTS_FILE, index=False)
        st.success("✅ Feedback submitted!")
    else:
        st.warning("❗ Please complete every field.")
