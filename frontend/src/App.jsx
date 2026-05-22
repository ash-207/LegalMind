import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';

import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import UploadPDF from './pages/UploadPDF';
import Documents from './pages/Documents';
import DocumentView from './pages/DocumentView';
import UploadAudio from './pages/UploadAudio';
import Transcriptions from './pages/Transcriptions';
import Assistant from './pages/Assistant';
import Profile from './pages/Profile';

function Layout({ children, hideNav }) {
  return (
    <>
      {!hideNav && <Navbar />}
      {children}
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Layout><Landing /></Layout>} />
          <Route path="/login" element={<Layout hideNav><Login /></Layout>} />
          <Route path="/register" element={<Layout hideNav><Register /></Layout>} />

          <Route path="/dashboard" element={<Layout><ProtectedRoute><Dashboard /></ProtectedRoute></Layout>} />
          <Route path="/documents/upload" element={<Layout><ProtectedRoute><UploadPDF /></ProtectedRoute></Layout>} />
          <Route path="/documents" element={<Layout><ProtectedRoute><Documents /></ProtectedRoute></Layout>} />
          <Route path="/documents/:id" element={<Layout><ProtectedRoute><DocumentView /></ProtectedRoute></Layout>} />
          <Route path="/transcriber/upload" element={<Layout><ProtectedRoute><UploadAudio /></ProtectedRoute></Layout>} />
          <Route path="/transcriptions" element={<Layout><ProtectedRoute><Transcriptions /></ProtectedRoute></Layout>} />
          <Route path="/assistant" element={<Layout><ProtectedRoute><Assistant /></ProtectedRoute></Layout>} />
          <Route path="/profile" element={<Layout><ProtectedRoute><Profile /></ProtectedRoute></Layout>} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
