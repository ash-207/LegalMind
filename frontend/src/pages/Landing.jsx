import { Link } from 'react-router-dom';
import './Landing.css';

const features = [
  { icon: '📄', title: 'PDF Summarizer', desc: 'Upload any legal document. Get structured summaries with key clauses, risks, and action items instantly.' },
  { icon: '🎙', title: 'Hearing Transcriber', desc: 'Upload court audio. Whisper AI transcribes it, then LegalMind extracts decisions and next steps.' },
  { icon: '⚡', title: 'AI Assistant', desc: 'Ask anything about your documents. Explain clauses, translate legal jargon, flag risks.' },
  { icon: '🔐', title: 'Secure & Private', desc: 'JWT-protected. Your documents stay yours. Built with Spring Boot + PostgreSQL.' },
];

export default function Landing() {
  return (
    <div className="landing">
      <section className="hero">
        <div className="hero-badge">AI-Powered Legal Intelligence</div>
        <h1 className="hero-title">
          Your legal documents,<br/>
          <span className="hero-accent">finally understood.</span>
        </h1>
        <p className="hero-sub">
          Upload PDFs. Transcribe hearings. Get structured summaries,<br />
          action items, and risk flags — in seconds.
        </p>
        <div className="hero-cta">
          <Link to="/register" className="btn-primary" style={{fontSize:'16px',padding:'14px 36px'}}>
            Start for Free →
          </Link>
          <Link to="/login" className="btn-outline" style={{fontSize:'16px',padding:'14px 36px'}}>
            Sign In
          </Link>
        </div>
      </section>

      <section className="features-section">
        <h2 className="section-title">Everything you need</h2>
        <div className="features-grid">
          {features.map(f => (
            <div key={f.title} className="feature-card">
              <span className="feature-icon">{f.icon}</span>
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="cta-section">
        <h2>Ready to simplify legal work?</h2>
        <p>Join legal professionals who use LegalMind to save hours every day.</p>
        <Link to="/register" className="btn-primary" style={{fontSize:'16px',padding:'14px 36px'}}>
          Get Started Free →
        </Link>
      </section>

      <footer className="footer">
        <span className="brand-name" style={{fontFamily:'Playfair Display, serif',color:'var(--espresso)'}}>⚖ LegalMind</span>
        <span style={{color:'var(--text-muted)',fontSize:'13px'}}>© 2025 LegalMind. All rights reserved.</span>
      </footer>
    </div>
  );
}
