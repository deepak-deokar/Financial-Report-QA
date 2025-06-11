// src/app/upload/page.tsx

'use client';

import { useState } from 'react';
import Spinner from '../../components/Spinner';

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setStatus('Uploading...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      console.log(data);
      setStatus(data.message || 'Uploaded successfully ✅');
    } catch (err) {
      console.error(err);
      setStatus('Error uploading file.');
    }

    setLoading(false);
    setFile(null);  // Clear after upload
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>📤 Upload Financial Document</h1>

      <div style={styles.inputContainer}>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          style={styles.fileInput}
        />
      </div>

      {file && <p style={styles.fileName}>Selected: {file.name}</p>}

      <div style={styles.buttonContainer}>
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          style={styles.button}
        >
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </div>

      <div style={styles.statusBox}>
        {loading ? <Spinner /> : <p>{status}</p>}
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
    marginBottom: '1.5rem',
  },
  fileInput: {
    padding: '0.5rem',
    fontSize: '1rem',
    borderRadius: '6px',
    border: '1px solid #ccc',
    width: '300px',
    cursor: 'pointer',
  },
  fileName: {
    marginBottom: '1rem',
    fontStyle: 'italic',
    color: '#555',
  },
  buttonContainer: {
    marginBottom: '2rem',
  },
  button: {
    padding: '0.75rem 1.5rem',
    fontSize: '1rem',
    backgroundColor: '#28a745',
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
  },
  statusBox: {
    marginTop: '1rem',
    minHeight: '50px',
    padding: '1rem',
    border: '1px solid #eee',
    borderRadius: '4px',
    backgroundColor: '#fafafa',
    color: '#333',
  },
};