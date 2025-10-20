import re
from pymongo import MongoClient
from deep_translator import GoogleTranslator
from textblob import TextBlob
from dotenv import load_dotenv
import os
import unicodedata

# 1️⃣ Load .env variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if not all([MONGO_URI, DB_NAME, COLLECTION_NAME]):
    raise ValueError("❌ Missing MONGO_URI, DB_NAME, or COLLECTION_NAME in .env")

# 2️⃣ Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# 3️⃣ Emoji + symbol remover
EMOJI_PATTERN = re.compile(
    "[" "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002700-\U000027BF"
    "\U000024C2-\U0001F251"
    "\U0001F900-\U0001F9FF"
    "\U0000200D"
    "]+", flags=re.UNICODE
)
SYMBOL_PATTERN = re.compile(r"[^\w\s\.,!?\-@#&():;\/'\"%$]")

def clean_text_field(s: str) -> str:
    """Remove emojis, unwanted symbols, normalize Unicode."""
    if not isinstance(s, str):
        return s
    s = EMOJI_PATTERN.sub("", s)
    s = SYMBOL_PATTERN.sub("", s)
    s = unicodedata.normalize("NFKC", s)  # normalize complex Indian scripts
    s = re.sub(r"\s+", " ", s).strip()
    return s

def translate_to_english(text):
    """Auto-detect and translate text to English."""
    try:
        translated = GoogleTranslator(source="auto", target="en").translate(text)
        return translated
    except Exception as e:
        print(f"⚠️ Translation failed: {e}")
        return text  # keep original text if translation fails

def analyze_sentiment(text):
    """Compute polarity and label."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    label = "positive" if polarity > 0.1 else "negative" if polarity < -0.1 else "neutral"
    return {"score": polarity, "label": label}

# 4️⃣ Process only docs having "text" field
for doc in collection.find({"text": {"$exists": True}}):
    text = doc.get("text", "").strip()

    if not text:
        print(f"⏭️ Skipping empty text for ID {doc['_id']}")
        continue

    try:
        # Clean + Translate
        cleaned = clean_text_field(text)
        translated = translate_to_english(cleaned)

        # Sentiment
        sentiment = analyze_sentiment(translated)

        # Update MongoDB
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"text": translated, "sentiment": sentiment}}
        )

        print(f"✅ Updated: {doc['_id']} | Translated: {translated[:60]}...")

    except Exception as e:
        print(f"⚠️ Error for ID {doc['_id']}: {e}")

print("🎯 All Hindi/Marathi/other texts translated to English and sentiment updated.")
