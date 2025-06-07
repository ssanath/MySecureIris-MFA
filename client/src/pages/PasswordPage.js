import React, { useState } from "react";
import axios from "axios";
import "./PasswordPage.css";

function PasswordPage() {
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handlePasswordSubmit = async () => {
    if (!password) {
      setMessage("❌ Please enter your password.");
      return;
    }

    try {
      const email = localStorage.getItem("email");
      const response = await axios.post("/api/auth/verify-password", {
        email,
        password,
      });

      if (response.data.success) {
        setMessage("✅ Password verified. Proceeding to Iris Scan...");
        setTimeout(() => {
          window.location.href = "/iris-register";
        }, 1500);
      } else {
        setMessage("❌ " + response.data.message);
      }
    } catch (error) {
      console.error("Password verification error:", error);
      setMessage("🚫 Failed to verify password. Server error.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Enter Password</h2>
        <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handlePasswordSubmit}>Submit Password</button>
        {message && <p className="message">{message}</p>}
      </div>
    </div>
  );
}

export default PasswordPage;
