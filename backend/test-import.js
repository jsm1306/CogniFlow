import mongoose from "mongoose";
import dotenv from "dotenv";
import importTweetsFromCSV from "./scrapetweets.js";

dotenv.config();
async function testImport() {
  try {
    await mongoose.connect(process.env.MONG_URI);
    console.log('✓ Connected to MongoDB');

    console.log('\nStarting CSV import...\n');
    const results = await importTweetsFromCSV();
    
    console.log('\n========== IMPORT SUMMARY ==========');
    console.log(`Total tweets imported: ${results.length}`);
    console.log('====================================\n');

    // Close connection
    await mongoose.connection.close();
    console.log('✓ MongoDB connection closed');
    
    process.exit(0);
  } catch (error) {
    console.error('❌ Error during import:', error);
    await mongoose.connection.close();
    process.exit(1);
  }
}

testImport();
