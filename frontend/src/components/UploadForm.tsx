// src/components/UploadForm.tsx

'use client';

import { useState } from 'react';
import Spinner from './Spinner';

export default function UploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    const res = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData,
    });

    if (res.ok) {
      setStatus('Upload successful!');
    } else {
      setStatus('Upload failed.');
    }
    setLoading(false);
  };

  return (
    <div>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button onClick={handleUpload}>Upload</button>
      {loading ? <Spinner /> : <p style={{ marginTop: '1rem' }}>{status}</p>}
    </div>
  );
}