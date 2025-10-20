# from pymongo import MongoClient
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from tqdm import tqdm

# # 1️⃣ Connect to MongoDB
# client = MongoClient("mongodb+srv://sindhuj1729:OIAAzL6gT0aB8BUX@cluster0.1xkktix.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# # 2️⃣ Replace with your actual database and collection names
# db = client["your_database_name"]        # e.g. "social_data"
# collection = db["your_collection_name"]  # e.g. "zomato_posts"

# # 3️⃣ Initialize the sentiment analyzer
# analyzer = SentimentIntensityAnalyzer()

# # 4️⃣ Find all documents where 'sentiment' is missing
# cursor = collection.find({"sentiment": {"$exists": False}})

# # 5️⃣ Analyze each document’s 'text' field
# for doc in tqdm(cursor, desc="Analyzing Sentiment"):
#     text = doc.get("text", "")
#     if text:
#         score = analyzer.polarity_scores(text)["compound"]

#         # Label sentiment
#         if score >= 0.05:
#             label = "positive"
#         elif score <= -0.05:
#             label = "negative"
#         else:
#             label = "neutral"

#         # 6️⃣ Update the document with score and label
#         collection.update_one(
#             {"_id": doc["_id"]},
#             {"$set": {"sentiment": {"score": score, "label": label}}}
#         )

# print("✅ Sentiment analysis completed successfully!")

from pymongo import MongoClient
from textblob import TextBlob
from dotenv import load_dotenv
import os

# --- Load environment variables ---
load_dotenv()

# --- MongoDB Connection ---
uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME")

if not all([uri, db_name, collection_name]):
    raise ValueError("❌ Missing MONGO_URI, DB_NAME, or COLLECTION_NAME in .env file")

client = MongoClient(uri)
db = client[db_name]
collection = db[collection_name]

# --- Process Documents ---
for doc in collection.find():
    text = doc.get("text", "")
    if text:
        sentiment_score = TextBlob(text).sentiment.polarity
        sentiment_label = (
            "positive" if sentiment_score > 0 else
            "negative" if sentiment_score < 0 else
            "neutral"
        )
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"sentiment": {"score": sentiment_score, "label": sentiment_label}}}
        )

print("✅ Sentiment analysis completed and saved to MongoDB!")
