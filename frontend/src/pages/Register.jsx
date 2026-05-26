import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
//import { signup } from '../api/auth';
import { signup } from "../api/authApi";
import { useAuth } from '../context/AuthContext';
import './Auth.css';

export default function Register() {
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const handle = e => setForm(p => ({ ...p, [e.target.name]: e.target.value }));

  const submit = async e => {
    e.preventDefault();
    setLoading(true); setError('');
    try {
      const res = await signup(form);
      loginUser(res.data.token, form.email);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.message || 'Signup failed');
    } finally { setLoading(false); }
  };

  return (
    <div className="auth-page">
      <div className="auth-card card">
        <div className="auth-logo">⚖ LegalMind</div>
        <h2 className="auth-title">Create account</h2>
        <p className="auth-sub">Start your free account today</p>
        <form onSubmit={submit}>
          <div className="form-group">
            <label className="label">Full Name</label>
            <input name="name" placeholder="Arjun Sharma" value={form.name} onChange={handle} required />
          </div>
          <div className="form-group">
            <label className="label">Email</label>
            <input name="email" type="email" placeholder="you@example.com" value={form.email} onChange={handle} required />
          </div>
          <div className="form-group">
            <label className="label">Password</label>
            <input name="password" type="password" placeholder="Min. 8 characters" value={form.password} onChange={handle} required />
          </div>
          {error && <p className="error">{error}</p>}
          <button className="btn-primary" style={{width:'100%',justifyContent:'center',marginTop:8}} type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Create Account →'}
          </button>
        </form>
        <p className="auth-footer">Have an account? <Link to="/login">Sign in</Link></p>
      </div>
    </div>
  );
}
