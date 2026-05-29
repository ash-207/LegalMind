import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getDocuments } from '../api/documentApi';
import './List.css';

export default function Documents() {
  const [docs, setDocs] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
  getDocuments()
    .then(r => {
      console.log(r);
      setDocs(r);
    })
    .catch(err => {
      console.error(err);
      setDocs([]);
    })
    .finally(() => setLoading(false));
}, []);

  const filtered = docs.filter(d =>
    d.title?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="page-wrap">
      <div className="list-header">
        <h1 className="page-title">My Documents</h1>
        <Link to="/documents/upload" className="btn-primary">+ Upload PDF</Link>
      </div>

      <input placeholder="Search documents..." value={search} onChange={e => setSearch(e.target.value)} style={{marginBottom:24,maxWidth:400}} />

      {loading ? (
        <div style={{display:'flex',justifyContent:'center',padding:48}}><div className="spinner"></div></div>
      ) : filtered.length === 0 ? (
        <div className="empty-state">
          <span>📄</span>
          <p>No documents yet. Upload your first PDF!</p>
          <Link to="/documents/upload" className="btn-primary">Upload PDF →</Link>
        </div>
      ) : (
        <div className="list-grid">
          {filtered.map(d => (
            <Link to={`/documents/${d.id}`} key={d.id} className="list-card card">
              <div className="list-card-icon">📄</div>
              <div className="list-card-body">
                <h3 className="list-card-title">{d.title}</h3>
                <p className="list-card-preview">{d.summary?.substring(0, 120)}...</p>
                <div className="list-card-meta">
                  <span className="chip">{new Date(d.uploadedAt).toLocaleDateString()}</span>
                  <span className="chip">{d.uploadedBy}</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
