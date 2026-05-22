import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Dashboard.css';

const cards = [
  { to: '/documents/upload', icon: '📄', label: 'Upload PDF', desc: 'Summarize a legal document', color: '#f5ede6' },
  { to: '/transcriber/upload', icon: '🎙', label: 'Upload Audio', desc: 'Transcribe a court hearing', color: '#eedfd5' },
  { to: '/documents', icon: '🗂', label: 'My Documents', desc: 'View all uploaded PDFs', color: '#e8cfc2' },
  { to: '/transcriptions', icon: '📝', label: 'Transcriptions', desc: 'View hearing transcripts', color: '#dfc0ae' },
  { to: '/assistant', icon: '⚡', label: 'AI Assistant', desc: 'Ask anything about your docs', color: '#d4af9f' },
  { to: '/profile', icon: '👤', label: 'Profile', desc: 'Your account settings', color: '#c9a090' },
];

export default function Dashboard() {
  const { user } = useAuth();
  const name = user?.email?.split('@')[0] || 'User';

  return (
    <div className="page-wrap">
      <div className="dash-header">
        <div>
          <h1 className="dash-title">Good day, {name} 👋</h1>
          <p style={{color:'var(--text-muted)',marginTop:4}}>What would you like to work on today?</p>
        </div>
      </div>

      <div className="dash-grid">
        {cards.map(c => (
          <Link to={c.to} key={c.to} className="dash-card" style={{background: c.color}}>
            <span className="dash-icon">{c.icon}</span>
            <h3>{c.label}</h3>
            <p>{c.desc}</p>
            <span className="dash-arrow">→</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
