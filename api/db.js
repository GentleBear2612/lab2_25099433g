const { MongoClient } = require('mongodb');

const uri = process.env.MONGO_URI;
const dbName = process.env.MONGO_DB_NAME || 'notetaker_db';

if (!uri) {
  // Don't throw at module load time to avoid build-time failures in some platforms,
  // but handlers will check and return an informative error.
  console.warn('MONGO_URI not set. API handlers will return 500 until MONGO_URI is configured.');
}

let cachedClient = global.__mongoClient; // cached across lambda invocations
let cachedDb = global.__mongoDb;

async function connect() {
  if (cachedDb) return cachedDb;
  if (!uri) throw new Error('MONGO_URI is not configured');

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
