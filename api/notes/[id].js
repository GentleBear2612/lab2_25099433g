const connect = require('../../api/db');
const { ObjectId } = require('mongodb');

module.exports = async (req, res) => {
  try {
    const { id } = req.query;
    if (!id) return res.status(400).json({ error: 'Missing id' });
    const db = await connect();
    const coll = db.collection('notes');

    if (req.method === 'GET') {
      const doc = await coll.findOne({ _id: new ObjectId(id) });
      if (!doc) return res.status(404).json({ error: 'Note not found' });
      return res.status(200).json({ id: doc._id.toString(), title: doc.title, content: doc.content, created_at: doc.created_at, updated_at: doc.updated_at, translations: doc.translations || {} });
    }

    if (req.method === 'PUT') {
      const data = req.body || {};
      const update = {};
      if (data.title) update.title = data.title;
      if (data.content) update.content = data.content;
      if (data.translations && typeof data.translations === 'object') {
        for (const [k, v] of Object.entries(data.translations)) {
          update[`translations.${k}`] = v;
        }
      }
      if (Object.keys(update).length === 0) return res.status(400).json({ error: 'No updatable fields provided' });
      update.updated_at = new Date();
      const result = await coll.findOneAndUpdate({ _id: new ObjectId(id) }, { $set: update }, { returnDocument: 'after' });
      if (!result.value) return res.status(404).json({ error: 'Note not found' });
      const doc = result.value;
      return res.status(200).json({ id: doc._id.toString(), title: doc.title, content: doc.content, created_at: doc.created_at, updated_at: doc.updated_at, translations: doc.translations || {} });
    }

    if (req.method === 'DELETE') {
      const r = await coll.deleteOne({ _id: new ObjectId(id) });
      if (r.deletedCount === 0) return res.status(404).json({ error: 'Note not found' });
      return res.status(204).end();
    }

    res.setHeader('Allow', 'GET, PUT, DELETE');
    return res.status(405).end('Method Not Allowed');
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message });
  }
};
