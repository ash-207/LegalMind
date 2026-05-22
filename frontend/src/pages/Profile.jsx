import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Profile() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => { logout(); navigate('/'); };

  return (
    <div className="page-wrap">
      <h1 style={{fontSize:28,color:'var(--dark-roast)',marginBottom:8}}>Profile</h1>
      <p style={{color:'var(--text-muted)',marginBottom:32}}>Your account information</p>

      <div className="card" style={{maxWidth:480}}>
        <div style={{display:'flex',alignItems:'center',gap:20,marginBottom:28}}>
          <div style={{width:64,height:64,borderRadius:'50%',background:'var(--mocha)',color:'var(--cream)',display:'flex',alignItems:'center',justifyContent:'center',fontSize:28,fontWeight:600}}>
            {user?.email?.[0]?.toUpperCase()}
          </div>
          <div>
            <h2 style={{fontSize:20,color:'var(--dark-roast)'}}>{user?.email?.split('@')[0]}</h2>
            <p style={{fontSize:14,color:'var(--text-muted)'}}>{user?.email}</p>
          </div>
        </div>

        <div style={{display:'flex',flexDirection:'column',gap:14,borderTop:'1px solid var(--border)',paddingTop:20}}>
          <div style={{display:'flex',justifyContent:'space-between',fontSize:14}}>
            <span style={{color:'var(--text-muted)'}}>Email</span>
            <span style={{fontWeight:500}}>{user?.email}</span>
          </div>
          <div style={{display:'flex',justifyContent:'space-between',fontSize:14}}>
            <span style={{color:'var(--text-muted)'}}>Role</span>
            <span className="chip">USER</span>
          </div>
        </div>

        <button className="btn-outline" onClick={handleLogout} style={{marginTop:28,width:'100%',justifyContent:'center'}}>
          Logout
        </button>
      </div>
    </div>
  );
}
