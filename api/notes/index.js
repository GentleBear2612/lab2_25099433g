const connect = require('../../api/db');
const { ObjectId } = require('mongodb');

module.exports = async (req, res) => {
  try {
    const db = await connect();
    const coll = db.collection('notes');

    if (req.method === 'GET') {
      const docs = await coll.find().sort({ updated_at: -1 }).toArray();
      const out = docs.map(d => ({ id: d._id.toString(), title: d.title, content: d.content, created_at: d.created_at, updated_at: d.updated_at, translations: d.translations || {} }));
      return res.status(200).json(out);
    }

    if (req.method === 'POST') {
      const data = req.body || {};
      if (!data.title || !data.content) return res.status(400).json({ error: 'Title and content are required' });
      const now = new Date();
      const doc = { title: data.title, content: data.content, created_at: now, updated_at: now };
      const result = await coll.insertOne(doc);
      doc.id = result.insertedId.toString();
      return res.status(201).json({ id: doc.id, title: doc.title, content: doc.content, created_at: doc.created_at, updated_at: doc.updated_at, translations: {} });
    }

    res.setHeader('Allow', 'GET, POST');
    return res.status(405).end('Method Not Allowed');
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message });
  }
};
