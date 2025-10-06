import mongoose from "mongoose";
const Schema = mongoose.Schema;
const twitterSchema = new Schema(
  {
    text: String,
    created_at: String,
    sentiment: {
      label: String,
      score: Number,
    },
    hashtags: [String],
    location: String,
    engagement: Number, // likes + retweets combined
  },
  { timestamps: true }
);
const Twitter = mongoose.model("Twitter", twitterSchema);
export default Twitter;
