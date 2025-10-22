import mongoose from 'mongoose';
import dotenv from 'dotenv';
import Twitter from './Models/twitter.js';

dotenv.config();

const cities = [
  'Mumbai',
  'Delhi',
  'Kolkata',
  'Chennai',
  'Bengaluru',
  'Hyderabad',
  'Ahmedabad',
  'Pune',
  'Surat',
  'Jaipur',
  'Lucknow',
  'Indore',
  'Kanpur',
  'Nagpur',
  'Patna'
];

const updateTwitterLocations = async () => {
  try {
    // Connect to MongoDB
    await mongoose.connect(process.env.MONG_URI);
    console.log('Connected to MongoDB for Twitter update');

    // Get all Twitter documents
    const tweets = await Twitter.find({});
    console.log(`Found ${tweets.length} tweets to update`);

    // Update each tweet with a random city and format created_at
    for (let i = 0; i < tweets.length; i++) {
      const randomCity = cities[Math.floor(Math.random() * cities.length)];
      const createdAt = tweets[i].created_at;
      let formattedDate = null;
      if (createdAt) {
        const date = new Date(createdAt);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        formattedDate = `${day}-${month}-${year}`;
      }
      tweets[i].location = randomCity;
      tweets[i].created_at = formattedDate;
      await tweets[i].save();
      console.log(`Updated tweet ${i + 1}/${tweets.length}: location=${randomCity}, created_at=${formattedDate}`);
    }

    console.log('All Twitter locations and created_at dates updated successfully');
  } catch (error) {
    console.error('Error updating Twitter locations:', error);
  } finally {
    // Close the connection
    await mongoose.connection.close();
    console.log('Twitter database connection closed');
  }
};

const updateRedditLocations = async () => {
  try {
    // Connect to MongoDB Reddit database
    await mongoose.connect(process.env.MONG_URI);
    const redditDb = mongoose.connection.useDb('Reddit');
    const redditCollection = redditDb.collection('reddit');
    console.log('Connected to MongoDB for Reddit update');

    // Get all Reddit documents
    const redditPosts = await redditCollection.find({}).toArray();
    console.log(`Found ${redditPosts.length} Reddit posts to update`);

    // Update each Reddit post with a random city and format created_at
    for (let i = 0; i < redditPosts.length; i++) {
      const randomCity = cities[Math.floor(Math.random() * cities.length)];
      const createdAt = redditPosts[i].created_at;
      let formattedDate = null;
      if (createdAt) {
        const date = new Date(createdAt);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        formattedDate = `${day}-${month}-${year}`;
      }
      await redditCollection.updateOne(
        { _id: redditPosts[i]._id },
        { $set: { location: randomCity, created_at: formattedDate } }
      );
      console.log(`Updated Reddit post ${i + 1}/${redditPosts.length}: location=${randomCity}, created_at=${formattedDate}`);
    }

    console.log('All Reddit locations and created_at dates updated successfully');
  } catch (error) {
    console.error('Error updating Reddit locations:', error);
  } finally {
    // Close the connection
    await mongoose.connection.close();
    console.log('Reddit database connection closed');
  }
};

// Run both update functions
const runUpdates = async () => {
  await updateTwitterLocations();
  // await updateRedditLocations();
};

runUpdates();
