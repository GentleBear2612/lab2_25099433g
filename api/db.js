const { MongoClient } = require('mongodb');

// Prefer MONGODB_URI (some hosts) but fall back to MONGO_URI for compatibility
const uri = process.env.MONGODB_URI || process.env.MONGO_URI;
const dbName = process.env.MONGO_DB_NAME || 'notetaker_db';

if (!uri) {
  // Don't throw at module load time to avoid build-time failures in some platforms,
  // but handlers will check and return an informative error.
  console.warn('MONGODB_URI / MONGO_URI not set. API handlers will return 500 until configured.');
}

let cachedClient = global.__mongoClient; // cached across lambda invocations
let cachedDb = global.__mongoDb;

async function connect() {
  if (cachedDb) return cachedDb;
  if (!uri) throw new Error('MONGODB_URI / MONGO_URI is not configured');

  if (!cachedClient) {
    cachedClient = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    await cachedClient.connect();
  }

  cachedDb = cachedClient.db(dbName);
  global.__mongoClient = cachedClient;
  global.__mongoDb = cachedDb;
  return cachedDb;
}

module.exports = connect;
