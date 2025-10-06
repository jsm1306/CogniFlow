import express from 'express';
import Twitter from '../Models/twitter.js';
import importTweetsFromCSV from '../scrapetweets.js';

const router = express.Router();

// POST import tweets from CSV
router.post('/twitter/import', async (req, res) => {
  try {
    console.log('Starting CSV import...');
    const results = await importTweetsFromCSV();
    res.status(200).json({ 
      message: 'CSV import completed', 
      imported: results.length,
      tweets: results 
    });
  } catch (error) {
    console.error('Import error:', error);
    res.status(500).json({ message: 'Error importing CSV', error: error.message });
  }
});

// GET all twitter entries
router.get('/twitter', async (req, res) => {
  try {
    const tweets = await Twitter.find();
    res.json(tweets);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// GET twitter entry by id
router.get('/twitter/:id', async (req, res) => {
  try {
    const tweet = await Twitter.findById(req.params.id);
    if (!tweet) {
      return res.status(404).json({ message: 'Tweet not found' });
    }
    res.json(tweet);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// POST create new twitter entry
router.post('/twitter', async (req, res) => {
  const tweet = new Twitter({
    text: req.body.text,
    created_at: req.body.created_at,
    sentiment: req.body.sentiment,
    hashtags: req.body.hashtags,
    location: req.body.location,
    engagement: req.body.engagement
  });

  try {
    const newTweet = await tweet.save();
    res.status(201).json(newTweet);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

// PUT update twitter entry by id
router.put('/twitter/:id', async (req, res) => {
  try {
    const tweet = await Twitter.findById(req.params.id);
    if (!tweet) {
      return res.status(404).json({ message: 'Tweet not found' });
    }

    tweet.text = req.body.text || tweet.text;
    tweet.created_at = req.body.created_at || tweet.created_at;
    tweet.sentiment = req.body.sentiment || tweet.sentiment;
    tweet.hashtags = req.body.hashtags || tweet.hashtags;
    tweet.location = req.body.location || tweet.location;
    tweet.engagement = req.body.engagement || tweet.engagement;

    const updatedTweet = await tweet.save();
    res.json(updatedTweet);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

// DELETE twitter entry by id
router.delete('/twitter/:id', async (req, res) => {
  try {
    const tweet = await Twitter.findById(req.params.id);
    if (!tweet) {
      return res.status(404).json({ message: 'Tweet not found' });
    }

    await tweet.remove();
    res.json({ message: 'Tweet deleted' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

export default router;
