import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getTranscriptions } from '../api/transcriptionApi';
import './List.css';

export default function Transcriptions() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
  getTranscriptions()
    .then(data => {
      console.log(data);
      setItems(data);
    })
    .catch(err => {
      console.error(err);
      setItems([]);
    })
    .finally(() => setLoading(false));
}, []);

  return (
    <div className="page-wrap">
      <div className="list-header">
        <h1 className="page-title">Transcriptions</h1>
        <Link to="/transcriber/upload" className="btn-primary">+ Upload Audio</Link>
      </div>

      {loading ? (
        <div style={{display:'flex',justifyContent:'center',padding:48}}><div className="spinner"></div></div>
      ) : items.length === 0 ? (
        <div className="empty-state">
          <span>🎙</span>
          <p>No transcriptions yet. Upload a hearing audio!</p>
          <Link to="/transcriber/upload" className="btn-primary">Upload Audio →</Link>
        </div>
      ) : (
        <div className="list-grid">
          {items.map(t => (
            <Link to={`/transcriptions/${t.id}`} key={t.id} className="list-card card">
              <div className="list-card-icon">🎙</div>
              <div className="list-card-body">
                <h3 className="list-card-title">{t.title || t.fileName || 'Hearing'}</h3>
                <p className="list-card-preview">{t.transcription?.substring(0, 120)}...</p>
                <div className="list-card-meta">
                <span className="chip">
                  {new Date(t.uploadedAt).toLocaleDateString()}
                </span>
                        
                <span className="chip">
                  {t.uploadedBy}
                </span>
              </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
