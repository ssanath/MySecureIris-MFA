import React, { useState } from 'react';
import axios from 'axios';

function IrisRegisterPage() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleIrisRegister = async () => {
    setLoading(true);
    setMessage('');
    try {
      const res = await axios.post('/api/iris/register');
      if (res.data.success) {
        setMessage('✅ Iris registered successfully!');
        setTimeout(() => {
          window.location.href = '/iris-verify';
        }, 1500);
      } else {
        setMessage('❌ ' + res.data.message);
      }
    } catch (err) {
      console.error('Iris registration error:', err);
      setMessage('❌ Iris registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '100px auto', background: '#111', color: 'white', padding: 20, borderRadius: 10, textAlign: 'center' }}>
      <h2>Iris Registration</h2>
      <button
        onClick={handleIrisRegister}
        disabled={loading}
        style={{ padding: 10, backgroundColor: '#3f51b5', color: 'white', border: 'none', borderRadius: 5 }}
      >
        {loading ? 'Scanning...' : 'Scan & Register Iris'}
      </button>
      <p>{message}</p>
    </div>
  );
}

export default IrisRegisterPage;
