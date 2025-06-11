'use client';

import { useState } from 'react';
import Spinner from '../components/Spinner';

export default function Page() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    const res = await fetch('http://localhost:8000/hybrid_rag', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: query }),
    });
    const data = await res.json();
    setResponse(data.answer || 'No answer');
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>📊 Financial Document Q&A Assistant 🗨️</h1>
      <div style={styles.inputContainer}>
        <input
          type="text"
          placeholder="Ask a question about your document..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          style={styles.button}
        >
          {loading ? 'Thinking...' : 'Submit'}
        </button>
      </div>
      <div style={styles.responseBox}>
        {loading ? <Spinner /> : <p>{response}</p>}
      </div>
    </div>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    maxWidth: '800px',
    margin: '3rem auto',
    padding: '2rem',
    borderRadius: '8px',
    border: '1px solid #ddd',
    boxShadow: '0 4px 10px rgba(0,0,0,0.1)',
    fontFamily: 'Arial, sans-serif',
    textAlign: 'center',
  },
  title: {
    textAlign: 'center',
    color: '#333',
    marginBottom: '2rem',
  },
  inputContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    gap: '1rem',
    marginBottom: '2rem',
    flexWrap: 'wrap',
  },
  input: {
    width: '400px',
    height: '48px',
    padding: '0 1rem',
    fontSize: '1rem',
    borderRadius: '4px',
    border: '1px solid #ccc',
    verticalAlign: 'middle',
  },
  button: {
    margin: '0',
    height: '48px',
    padding: '0 1rem',
    fontSize: '1rem',
    backgroundColor: '#0070f3',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    verticalAlign: 'middle',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    minWidth: '120px',
  },
  responseBox: {
    minHeight: '100px',
    padding: '1rem',
    border: '1px solid #eee',
    borderRadius: '4px',
    backgroundColor: '#fafafa',
    color: '#333',
  },
};