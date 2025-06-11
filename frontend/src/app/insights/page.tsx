'use client';

import { useState } from 'react';
import Spinner from '../../components/Spinner';

export default function InsightsPage() {
  const [query, setQuery] = useState('');
  const [insights, setInsights] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/insights', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: query }),
      });
      const data = await res.json();
      setInsights(data.insights || 'No insights generated');
    } catch (err) {
      console.error(err);
      setInsights('Error connecting to API.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>📈 Generate Financial Insights 🧠</h1>

      <div style={styles.inputContainer}>
        <input
          type="text"
          placeholder="Ask for insights..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
        />
        <button onClick={handleSubmit} disabled={loading} style={styles.button}>
          {loading ? 'Generating...' : 'Submit'}
        </button>
      </div>

      <div style={styles.responseBox}>
        {loading ? <Spinner /> : <p>{insights}</p>}
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
  },
  title: {
    textAlign: 'center',
    color: '#333',
    marginBottom: '2rem',
  },
  inputContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center', // this is correct
    gap: '1rem',
    marginBottom: '2rem',
    flexWrap: 'wrap',
  },
  input: {
    width: '400px',
    height: '48px', // ADD THIS
    padding: '0 1rem',
    fontSize: '1rem',
    borderRadius: '4px',
    border: '1px solid #ccc',
    verticalAlign: 'middle', // ADD THIS
  },
  button: {
    margin: '0',
    height: '48px', // ADD THIS
    padding: '0 1rem',
    fontSize: '1rem',
    backgroundColor: '#0070f3',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    verticalAlign: 'middle', // ADD THIS
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