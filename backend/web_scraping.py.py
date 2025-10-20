import os
import uuid
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
import praw
from textblob import TextBlob

# Load environment variables from .env file
load_dotenv()

# Fetch secrets from the environment variables
MONG_URI = os.getenv("MONG_URI")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Check if any of the environment variables are missing
if not all([MONG_URI, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
    print("❌ Missing one or more environment variables. Please check your .env file.")
    exit(1)

# Connect to MongoDB
try:
    client = MongoClient(MONG_URI)
    db = client['Reddit']  # MongoDB database name
    collection = db['reddit']  # MongoDB collection name (updated)
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print("❌ Error connecting to MongoDB:", e)
    exit(1)

# Initialize Reddit API using praw
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Define search query and limit
query = "zomato review"
limit = 200  # Fetch 200 posts

results = []

# Fetch posts from Reddit
for post in reddit.subreddit("all").search(query, limit=limit):
    if not post.selftext:
        continue

    # Sentiment analysis using TextBlob
    sentiment = TextBlob(post.selftext).sentiment
    polarity = sentiment.polarity
    label = "positive" if polarity > 0 else ("negative" if polarity < 0 else "neutral")

    # Store the post details in a dictionary
    data = {
        "_id": str(uuid.uuid4()),  # Unique ID for the post
        "subreddit": post.subreddit.display_name,
        "title": post.title,
        "text": post.selftext,
        "created_at": datetime.utcfromtimestamp(post.created_utc),  # UTC timestamp
        "sentiment": {
            "label": label,
            "score": polarity
        },
        "upvotes": post.score  # Upvotes for the post
    }

    # Append the post data to the results list
    results.append(data)

# Insert scraped posts into MongoDB collection
if results:
    try:
        collection.insert_many(results)
        print(f"✅ Inserted {len(results)} documents into MongoDB")
    except Exception as e:
        print("❌ Error inserting documents into MongoDB:", e)
else:
    print("No data to insert")

# Save the scraped data to an Excel file with a new sheet
df = pd.DataFrame(results)
df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Write to Excel file, appending data to a new sheet
excel_filename = "zomato_reddit_reviews.xlsx"
with pd.ExcelWriter(excel_filename, engine='openpyxl', mode='a') as writer:
    df.to_excel(writer, sheet_name="Reddit_Reviews_200", index=False)

print(f"✅ Done! Data saved to {excel_filename} in a new sheet.")

# --------------------

# import os
# import uuid
# from datetime import datetime
# import pandas as pd
# from dotenv import load_dotenv
# import praw
# from textblob import TextBlob

# # Load environment variables from .env
# load_dotenv()

# # Fetch Reddit API credentials
# REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
# REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
# REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# # Check credentials
# if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
#     print("❌ Missing Reddit API credentials. Check your .env file.")
#     exit(1)

# # Initialize Reddit API
# reddit = praw.Reddit(
#     client_id=REDDIT_CLIENT_ID,
#     client_secret=REDDIT_CLIENT_SECRET,
#     user_agent=REDDIT_USER_AGENT
# )

# # Search query and post limit
# query = "zomato review"
# limit = 200

# results = []

# # Fetch Reddit posts
# for post in reddit.subreddit("all").search(query, limit=limit):
#     if not post.selftext:
#         continue

#     sentiment = TextBlob(post.selftext).sentiment
#     polarity = sentiment.polarity
#     label = "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"

#     results.append({
#         "uuid": str(uuid.uuid4()),
#         "subreddit": post.subreddit.display_name,
#         "title": post.title,
#         "text": post.selftext,
#         "created_at": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
#         "sentiment_label": label,
#         "sentiment_score": polarity,
#         "upvotes": post.score
#     })

# # Convert to DataFrame
# df = pd.DataFrame(results)

# # Generate new filename with timestamp
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# filename = f"zomato_reddit_reviews_{timestamp}.xlsx"

# # Save to new Excel file
# df.to_excel(filename, sheet_name="Reddit_Reviews_200", index=False)

# print(f"✅ Data saved to new Excel file: {filename}")

# -------------------

# import os
# import uuid
# from datetime import datetime
# import pandas as pd
# from dotenv import load_dotenv
# from pymongo import MongoClient
# import praw
# from textblob import TextBlob

# # Load env variables from .env
# load_dotenv()

# # Fetch secrets from env
# MONG_URI = os.getenv("MONG_URI")
# REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
# REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
# REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# if not all([MONG_URI, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
#     print("❌ Missing one or more environment variables. Please check your .env file.")
#     exit(1)

# # Connect to MongoDB
# client = MongoClient(MONG_URI)
# db = client['Reddit']          # Database name
# collection = db['posts']       # Collection name

# # Initialize Reddit API
# reddit = praw.Reddit(
#     client_id=REDDIT_CLIENT_ID,
#     client_secret=REDDIT_CLIENT_SECRET,
#     user_agent=REDDIT_USER_AGENT
# )

# query = "zomato review"
# limit = 100

# results = []

# for post in reddit.subreddit("all").search(query, limit=limit):
#     if not post.selftext:
#         continue

#     sentiment = TextBlob(post.selftext).sentiment
#     polarity = sentiment.polarity
#     label = "positive" if polarity > 0 else ("negative" if polarity < 0 else "neutral")

#     data = {
#         "_id": str(uuid.uuid4()),
#         "subreddit": post.subreddit.display_name,
#         "title": post.title,
#         "text": post.selftext,
#         "created_at": datetime.utcfromtimestamp(post.created_utc),
#         "sentiment": {
#             "label": label,
#             "score": polarity
#         },
#         "upvotes": post.score
#     }

#     results.append(data)

# # Insert scraped posts into MongoDB collection
# if results:
#     try:
#         collection.insert_many(results)
#         print(f"✅ Inserted {len(results)} documents into MongoDB")
#     except Exception as e:
#         print("❌ Error inserting documents:", e)
# else:
#     print("No data to insert")

# # Save to Excel as well (optional)
# df = pd.DataFrame(results)
# df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
# df.to_excel("zomato_reddit_reviews.xlsx", index=False)
# print("✅ Done! Data saved to zomato_reddit_reviews.xlsx")
