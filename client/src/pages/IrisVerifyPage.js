import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./IrisVerifyPage.css";

export default function IrisVerifyPage() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const API = process.env.REACT_APP_BACKEND_URL;

  const handleVerify = async () => {
    setLoading(true);
    setMessage("");

    try {
      const res = await axios.post(`${API}/api/iris/verify`, {}, { withCredentials: true });
      if (res.data.success) {
        setMessage("✅ Iris verified successfully!");
        setTimeout(() => {
          navigate("/dashboard");
        }, 1500);
      } else {
        setMessage("❌ " + res.data.message);
      }
    } catch (err) {
      console.error("Iris verification error:", err);
      setMessage("❌ Iris verification failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="iris-verify-container">
      <div className="iris-verify-card">
        <h2>Iris Verification</h2>
        <button onClick={handleVerify} disabled={loading}>
          {loading ? "Verifying..." : "Verify Iris"}
        </button>
        <p className="message">{message}</p>
      </div>
    </div>
  );
}
