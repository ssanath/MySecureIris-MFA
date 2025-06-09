import React, { useState } from 'react';
import axios from 'axios';
import './IrisRegisterPage.css';

function IrisRegisterPage() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const API = process.env.REACT_APP_BACKEND_URL;

  const handleIrisRegister = async () => {
    setLoading(true);
    setMessage('');
    try {
      const res = await axios.post(`${API}/api/iris/register`, {}, { withCredentials: true });
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
    <div className="iris-register-container">
      <div className="iris-card">
        <h2>Iris Registration</h2>
        <button onClick={handleIrisRegister} disabled={loading}>
          {loading ? 'Scanning...' : 'Scan & Register Iris'}
        </button>
        {message && <p className="message">{message}</p>}
      </div>
    </div>
  );
}

export default IrisRegisterPage;
