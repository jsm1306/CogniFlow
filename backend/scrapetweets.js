import csv from 'csv-parser';
import fs from 'fs';
import Twitter from "./Models/twitter.js";

async function importTweetsFromCSV() {
  const tweetsToSave = [];
  let processedCount = 0;
  let savedCount = 0;

  return new Promise((resolve, reject) => {
    const stream = fs.createReadStream('n8n X Sheet - Sheet1.csv')
      .pipe(csv());

    stream.on('error', (err) => {
      console.error('Error reading CSV file:', err);
      reject(err);
    });

    stream.on('data', (row) => {
      try {
        // Fixed regex pattern - single backslash
        const hashtags = (row['Text Content'].match(/#\w+/g) || []).map(tag => tag.substring(1));
        const engagement = parseInt(row['Reply Count'] || 0) + parseInt(row['Like Count'] || 0);

        const tweet = new Twitter({
          text: row['Text Content'],
          created_at: row['Date'],
          hashtags,
          engagement,
          location: row['Tweet by'] || row['Profile User Name'],
          sentiment: { label: '', score: 0 } // calculate separately
        });

        processedCount++;
        
        // Store the save promise with proper error handling
        const savePromise = tweet.save()
          .then((savedTweet) => {
            savedCount++;
            console.log(`Saved tweet ${savedCount}/${processedCount}`);
            return savedTweet;
          })
          .catch(err => {
            console.error('Error saving tweet:', err.message);
            console.error('Tweet data:', {
              text: row['Text Content']?.substring(0, 50) + '...',
              date: row['Date']
            });
            return null; // Return null for failed saves
          });

        tweetsToSave.push(savePromise);
      } catch (err) {
        console.error('Error processing row:', err.message, row);
      }
    });

    stream.on('end', async () => {
      try {
        console.log(`\nFinished reading CSV. Processing ${tweetsToSave.length} tweets...`);
        
        // Wait for all save operations to complete
        const results = await Promise.all(tweetsToSave);
        
        // Filter out null values (failed saves)
        const successfulSaves = results.filter(result => result !== null);
        
        console.log(`\n✓ Successfully saved ${successfulSaves.length} out of ${tweetsToSave.length} tweets to MongoDB`);
        
        if (successfulSaves.length < tweetsToSave.length) {
          console.log(`✗ Failed to save ${tweetsToSave.length - successfulSaves.length} tweets`);
        }
        
        resolve(successfulSaves);
      } catch (err) {
        console.error('Error during save operation:', err);
        reject(err);
      }
    });
  });
}

export default importTweetsFromCSV;
