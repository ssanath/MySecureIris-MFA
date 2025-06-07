import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function IrisVerifyPage() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleVerify = async () => {
    setLoading(true);
    setMessage("");

    try {
      const res = await axios.post("/api/iris/verify");
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
