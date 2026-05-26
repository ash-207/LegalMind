import { useState, useRef } from 'react';
//import { uploadDocument } from '../api/documents';
import { uploadPdf } from "../api/documentApi";
import './Upload.css';

export default function UploadPDF() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [drag, setDrag] = useState(false);
  const inputRef = useRef();

  const handleFile = f => {
    if (f && f.type === 'application/pdf') { setFile(f); setError(''); }
    else setError('Please select a PDF file.');
  };

  const submit = async () => {

    if (!file) return;
    setLoading(true);
    setError('');
    setResult(null);

    try {
        const res =
            await uploadPdf(file);
        setResult(res);
    } catch (err) {
        setError(
            err.response?.data?.summary
            || 'Upload failed.'
        );
    } finally {
        setLoading(false);
    }
};

  return (
    <div className="page-wrap">
      <h1 className="page-title">Upload Legal PDF</h1>
      <p className="page-sub">Upload a legal document to get an AI-powered summary.</p>

      <div className={`drop-zone card ${drag ? 'drag-over' : ''}`}
        onClick={() => inputRef.current.click()}
        onDragOver={e => { e.preventDefault(); setDrag(true); }}
        onDragLeave={() => setDrag(false)}
        onDrop={e => { e.preventDefault(); setDrag(false); handleFile(e.dataTransfer.files[0]); }}>
        <input ref={inputRef} type="file" accept=".pdf" hidden onChange={e => handleFile(e.target.files[0])} />
        <span className="drop-icon">📄</span>
        {file ? (
          <div>
            <p className="drop-filename">{file.name}</p>
            <p className="drop-size">{(file.size / 1024).toFixed(1)} KB</p>
          </div>
        ) : (
          <div>
            <p className="drop-label">Drop your PDF here</p>
            <p className="drop-hint">or click to browse</p>
          </div>
        )}
      </div>

      {error && <p className="error" style={{marginTop:12}}>{error}</p>}

      <button className="btn-primary" style={{marginTop:20}} onClick={submit} disabled={!file || loading}>
        {loading ? <><span className="spinner" style={{width:18,height:18,borderWidth:2}}></span> Processing...</> : 'Summarize →'}
      </button>

      {result && (
        <div className="card result-card">
          <div className="result-meta">
            <span className="chip">{result.uploadedBy}</span>
            <span className="chip">{new Date(result.uploadedAt).toLocaleDateString()}</span>
          </div>
          <h2 className="result-title">{result.title}</h2>
          <h3 style={{fontSize:16,marginBottom:12,color:'var(--mocha)'}}>Summary</h3>
          <p className="result-text">{result.summary}</p>
        </div>
      )}
    </div>
  );
}
