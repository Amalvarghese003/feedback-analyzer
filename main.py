import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Step 1: Load feedback data from CSV
df = pd.read_csv('feedback.csv')

# Step 2: Define a function to analyze sentiment
def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Step 3: Apply the function to every feedback
df['Sentiment'] = df['Feedback_Text'].apply(get_sentiment)

# Step 4: Print results
print("Sentiment Analysis Results:")
print(df[['Feedback_Text', 'Sentiment']])

# Step 5: Show pie chart of sentiment distribution
df['Sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['green', 'red', 'orange'])
plt.title("Feedback Sentiment Distribution")
plt.ylabel("")
plt.show()

df.to_csv('results.csv', index=False)
print("\nResults saved to results.csv ✅")
