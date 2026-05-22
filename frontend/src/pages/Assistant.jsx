import { useState, useRef, useEffect } from 'react';
import api from '../api/client';
import './Assistant.css';

export default function Assistant() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I\'m your legal AI assistant. Ask me to explain clauses, summarize contracts, identify risks, or translate legal jargon.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef();

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg = { role: 'user', content: input };
    setMessages(p => [...p, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.post('/api/ai/chat', { message: input });
      setMessages(p => [...p, { role: 'assistant', content: res.data.reply || res.data.message }]);
    } catch {
      setMessages(p => [...p, { role: 'assistant', content: 'Sorry, I couldn\'t process that. Make sure the AI service is running.' }]);
    } finally { setLoading(false); }
  };

  const suggestions = ['Explain IPC Section 420', 'What are common bail conditions?', 'Translate "ex-parte" in simple terms', 'What is a non-bailable warrant?'];

  return (
    <div className="assistant-wrap">
      <div className="assistant-header">
        <h1>⚡ AI Legal Assistant</h1>
        <p>Ask anything about legal documents or concepts</p>
      </div>

      <div className="chat-window">
        {messages.map((m, i) => (
          <div key={i} className={`chat-msg ${m.role}`}>
            <div className="chat-bubble">{m.content}</div>
          </div>
        ))}
        {loading && (
          <div className="chat-msg assistant">
            <div className="chat-bubble typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {messages.length === 1 && (
        <div className="suggestions">
          {suggestions.map(s => (
            <button key={s} className="suggestion-chip" onClick={() => setInput(s)}>{s}</button>
          ))}
        </div>
      )}

      <div className="chat-input-row">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && send()}
          placeholder="Ask anything about legal terms, documents, clauses..."
        />
        <button className="btn-primary" onClick={send} disabled={loading || !input.trim()}>Send</button>
      </div>
    </div>
  );
}
