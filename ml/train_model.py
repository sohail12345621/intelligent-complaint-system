import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib, os

df = pd.read_csv("data/complaints.csv")

vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(df["text"])
y = df["category"]

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/category_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("Model trained and saved.")
