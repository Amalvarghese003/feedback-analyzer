import streamlit as st
import pandas as pd
import os

# ---------- Load feedback ----------
RESULTS_FILE = "results.csv"

if os.path.exists(RESULTS_FILE):
    results_df = pd.read_csv(RESULTS_FILE)
else:
    results_df = pd.DataFrame()  # empty

st.title("🔐 Admin Feedback Dashboard")

password = st.text_input("Enter admin password", type="password")

if password == "admin123":       # ← change to your own secure password
    st.success("Access granted. Welcome Admin!")
    if not results_df.empty:
        st.subheader("📄 All Submitted Feedback")
        st.dataframe(results_df)
    else:
        st.info("No feedback submitted yet.")
else:
    st.info("Only admins can view this page.")
