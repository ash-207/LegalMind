import { useState, useRef } from 'react';
//import { uploadAudio } from '../api/transcriptions';
import { uploadAudio } from "../api/transcriptionApi";
import './Upload.css';

const FORMATS = ['audio/mpeg','audio/wav','audio/mp4','audio/ogg','audio/flac','audio/webm'];

export default function UploadAudio() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [drag, setDrag] = useState(false);
  const inputRef = useRef();

  const handleFile = f => {
    if (f && FORMATS.includes(f.type)) { setFile(f); setError(''); }
    else setError('Please select an audio file (mp3, wav, m4a, etc.)');
  };

  const submit = async () => {


    if (!file) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {

        const res =
            await uploadAudio(file);

        setResult(res);

    } catch (err) {

        setError(
            err.response?.data?.detail
            || 'Transcription failed.'
        );

    } finally {

        setLoading(false);
    }
};

  return (
    <div className="page-wrap">
      <h1 className="page-title">Transcribe Court Hearing</h1>
      <p className="page-sub">Upload audio to get a transcript + structured legal summary.</p>

      <div className={`drop-zone card ${drag ? 'drag-over' : ''}`}
        onClick={() => inputRef.current.click()}
        onDragOver={e => { e.preventDefault(); setDrag(true); }}
        onDragLeave={() => setDrag(false)}
        onDrop={e => { e.preventDefault(); setDrag(false); handleFile(e.dataTransfer.files[0]); }}>
        <input ref={inputRef} type="file" accept="audio/*" hidden onChange={e => handleFile(e.target.files[0])} />
        <span className="drop-icon">🎙</span>
        {file ? (
          <div><p className="drop-filename">{file.name}</p><p className="drop-size">{(file.size/1024/1024).toFixed(2)} MB</p></div>
        ) : (
          <div><p className="drop-label">Drop audio here</p><p className="drop-hint">mp3 · wav · m4a · ogg · flac · webm</p></div>
        )}
      </div>

      {error && <p className="error" style={{marginTop:12}}>{error}</p>}

      <button className="btn-primary" style={{marginTop:20}} onClick={submit} disabled={!file || loading}>
        {loading ? <><span className="spinner" style={{width:18,height:18,borderWidth:2}}></span> Transcribing...</> : 'Transcribe →'}
      </button>

      {result && (
  <div className="card result-card">

    <h2 className="result-title">
      Transcript
    </h2>

    {result?.transcription && (
      <p className="result-text">
        {result.transcription}
      </p>
    )}

  </div>
)}
    </div>
  );
}
