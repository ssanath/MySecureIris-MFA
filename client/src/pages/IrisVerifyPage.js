import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // react-router-dom v6

export default function IrisVerifyPage() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();  // hook for navigation

  const handleVerify = async () => {
    setLoading(true);
    setMessage("");

    try {
      const res = await axios.post("http://localhost:5050/iris-verify");
      if (res.data.success) {
        setMessage("✅ Iris verified successfully!");
        // Redirect to dashboard after 1.5 seconds
        setTimeout(() => {
          navigate("/dashboard");
        }, 1500);
      } else {
        setMessage("❌ " + res.data.message);
      }
    } catch (err) {
      setMessage("❌ Iris verification failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: 400,
        margin: "100px auto",
        background: "#111",
        color: "white",
        padding: 20,
        borderRadius: 10,
        textAlign: "center",
      }}
    >
      <h2>Iris Verification</h2>
      <button
        onClick={handleVerify}
        disabled={loading}
        style={{
          padding: 10,
          backgroundColor: "#3f7a6f",
          color: "white",
          border: "none",
          borderRadius: 5,
        }}
      >
        {loading ? "Verifying..." : "Press 's' to scan & verify iris"}
      </button>
      <p>{message}</p>
    </div>
  );
}
