import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const loc = useLocation();

  const handleLogout = () => { logout(); navigate('/'); };

  const navLinks = [
    { to: '/dashboard', label: 'Dashboard' },
    { to: '/documents', label: 'Documents' },
    { to: '/transcriptions', label: 'Transcriptions' },
    { to: '/assistant', label: 'AI Assistant' },
  ];

  return (
    <nav className="navbar">
      <Link to={user ? '/dashboard' : '/'} className="navbar-brand">
        <span className="brand-icon">⚖</span>
        <span className="brand-name">LegalMind</span>
      </Link>

      {user ? (
        <div className="navbar-links">
          {navLinks.map(l => (
            <Link key={l.to} to={l.to}
              className={`nav-link ${loc.pathname.startsWith(l.to) ? 'active' : ''}`}>
              {l.label}
            </Link>
          ))}
          <Link to="/profile" className="nav-avatar">{user.email[0].toUpperCase()}</Link>
          <button className="btn-outline" style={{padding:'8px 18px',fontSize:'13px'}} onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <div className="navbar-links">
          <Link to="/login" className="btn-outline" style={{padding:'8px 20px',fontSize:'14px'}}>Login</Link>
          <Link to="/register" className="btn-primary" style={{padding:'8px 20px',fontSize:'14px'}}>Get Started</Link>
        </div>
      )}
    </nav>
  );
}
