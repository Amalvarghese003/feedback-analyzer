import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="AI Feedback Analyzer", page_icon="🧠")
st.title("🧠 Feedback Sentiment Analyzer")
st.subheader("Enter student feedback and instantly see if it's Positive, Negative, or Neutral.")

feedback = st.text_area("✍️ Enter Feedback:")

if st.button("Analyze Sentiment"):
    if feedback:
        analysis = TextBlob(feedback)
        polarity = analysis.sentiment.polarity

        if polarity > 0:
            st.success("😊 Sentiment: Positive")
        elif polarity < 0:
            st.error("😠 Sentiment: Negative")
        else:
            st.info("😐 Sentiment: Neutral")
    else:
        st.warning("⚠️ Please enter feedback before clicking Analyze.")
