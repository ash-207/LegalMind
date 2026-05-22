import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getDocument } from '../api/documents';

export default function DocumentView() {
  const { id } = useParams();
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDocument(id).then(r => setDoc(r.data)).catch(() => {}).finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="page-wrap" style={{display:'flex',justifyContent:'center',paddingTop:80}}><div className="spinner"></div></div>;
  if (!doc) return <div className="page-wrap"><p>Document not found. <Link to="/documents">Go back</Link></p></div>;

  return (
    <div className="page-wrap">
      <Link to="/documents" style={{color:'var(--mocha)',fontSize:14}}>← Back to Documents</Link>
      <h1 style={{fontSize:28,color:'var(--dark-roast)',margin:'16px 0 8px'}}>{doc.title}</h1>
      <div style={{display:'flex',gap:8,marginBottom:28}}>
        <span className="chip">{doc.uploadedBy}</span>
        <span className="chip">{new Date(doc.uploadedAt).toLocaleDateString()}</span>
      </div>

      <div className="card" style={{marginBottom:20}}>
        <h3 style={{fontSize:18,color:'var(--mocha)',marginBottom:14}}>AI Summary</h3>
        <p style={{color:'var(--text-muted)',lineHeight:1.8,whiteSpace:'pre-wrap'}}>{doc.summary}</p>
      </div>

      {doc.originalText && (
        <div className="card">
          <h3 style={{fontSize:18,color:'var(--mocha)',marginBottom:14}}>Extracted Text</h3>
          <p style={{color:'var(--text-muted)',lineHeight:1.8,fontSize:14,whiteSpace:'pre-wrap',maxHeight:400,overflowY:'auto'}}>{doc.originalText}</p>
        </div>
      )}
    </div>
  );
}
