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
